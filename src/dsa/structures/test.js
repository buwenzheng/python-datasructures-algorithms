// ==UserScript==
// @name         linux.do 阅读量刷新脚本
// @namespace    http://tampermonkey.net/
// @version      2025-04-23
// @description  try to take over the world!
// @author       You
// @match        https://linux.do/t/topic/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=linux.do
// @grant        none
// ==/UserScript==

(function () {
  "use strict";

  class AutoScroller {
    constructor() {
      this.scrollInterval = null;
      this.isScrolling = false;
      this.scrollDelay = 10000; // 10秒
      this.worker = null;
      // 定时与Worker
      // 滚动容器（默认文档）。会在初始化时自动检测可能的内滚容器
      this.scrollElement = null;

      // 配置（可在 UI 中调整，并持久化）
      this.config = {
        preheatMs: 10000, // 可见预热时长，毫秒
        bottomStableThreshold: 12, // 连续无增长计数
        bottomThreshold: 600, // 触底提前量，像素
      };
      this.loadConfig();

      // 到达底部的缓冲阈值（像素）。无限下拉时避免误判导致暂停
      this.bottomThreshold = this.config.bottomThreshold;
      // 末尾检测：接近底部且高度多次不增长则判定加载完毕
      this.lastKnownScrollHeight = 0;
      this.lastGrowthAt = Date.now();
      this.lastDomMutationAt = Date.now();
      this.bottomStableCount = 0;
      this.bottomStableThreshold = this.config.bottomStableThreshold; // 连续 N 次无增长即停止
      this.noGrowthMsThreshold = 120000; // 120s 无增长再判定
      this.nudgeInFlight = false;
      this.nudgeCount = 0;
      this.maxNudgesBeforePause = 3;

      this.initDomObserver();
      this.detectScrollElement();
      this.isPageHidden = document.hidden;
      this.suppressEndCheckUntil = 0;
      this.setupVisibilityHandlers();

      this.initStyles();
      this.createControlPanel();
      this.setupEventListeners();
      this.initWorker();
    }

    initStyles() {
      const style = document.createElement("style");
      style.textContent = `
                  #controlPanel {
                      position: fixed;
                      bottom: 20px;
                      left: 50%;
                      transform: translateX(-50%);
                      z-index: 100;
                      background: rgba(255,255,255,0.9);
                      padding: 10px 20px;
                      border-radius: 20px;
                      box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                      display: flex;
                      gap: 10px;
                  }

                  #controlPanel button {
                      padding: 8px 16px;
                      border: none;
                      border-radius: 5px;
                      background: #4a89dc;
                      color: white;
                      cursor: pointer;
                      transition: background 0.3s;
                  }

                  #controlPanel button:hover {
                      background: #3b7dd8;
                  }

                  #controlPanel button:disabled {
                      background: #cccccc;
                      cursor: not-allowed;
                  }

                  .status {
                      display: flex;
                      align-items: center;
                      padding: 0 10px;
                  }

                  .settings {
                      display: none;
                      align-items: center;
                      gap: 10px;
                  }

                  .settings.visible {
                      display: flex;
                  }

                  .settings label {
                      display: flex;
                      align-items: center;
                      gap: 4px;
                      background: rgba(0,0,0,0.04);
                      padding: 4px 8px;
                      border-radius: 6px;
                  }
              `;
      document.head.appendChild(style);
    }

    createControlPanel() {
      this.controlPanel = document.createElement("div");
      this.controlPanel.id = "controlPanel";

      this.startBtn = document.createElement("button");
      this.startBtn.id = "startBtn";
      this.startBtn.textContent = "开始滚动";

      this.pauseBtn = document.createElement("button");
      this.pauseBtn.id = "pauseBtn";
      this.pauseBtn.textContent = "暂停滚动";
      this.pauseBtn.disabled = true;

      const statusContainer = document.createElement("div");
      statusContainer.className = "status";
      statusContainer.innerHTML = '状态: <span id="statusText">暂停中</span>';

      this.statusText = statusContainer.querySelector("#statusText");

      // 设置开关和面板
      this.settingsToggleBtn = document.createElement("button");
      this.settingsToggleBtn.textContent = "设置";

      this.settingsPanel = document.createElement("div");
      this.settingsPanel.className = "settings";

      const preheatLabel = document.createElement("label");
      preheatLabel.title = "页面从隐藏恢复可见后，在此时间内不判定末尾";
      preheatLabel.innerHTML = `预热(s) <input id="cfgPreheat" type="number" min="0" max="600" step="1" style="width:70px"/>`;

      const stableLabel = document.createElement("label");
      stableLabel.title = "连续多少次接近底部且未增长，才认为可能到末尾";
      stableLabel.innerHTML = `稳定次数 <input id="cfgStable" type="number" min="1" max="100" step="1" style="width:70px"/>`;

      const bufferLabel = document.createElement("label");
      bufferLabel.title = "距离底部多少像素内就触发加载";
      bufferLabel.innerHTML = `提前量(px) <input id="cfgBuffer" type="number" min="0" max="5000" step="50" style="width:90px"/>`;

      this.settingsPanel.append(preheatLabel, stableLabel, bufferLabel);

      this.controlPanel.append(
        this.startBtn,
        this.pauseBtn,
        statusContainer,
        this.settingsToggleBtn,
        this.settingsPanel
      );
      document.body.appendChild(this.controlPanel);

      // 初始化输入值
      const preheatInput = this.settingsPanel.querySelector("#cfgPreheat");
      const stableInput = this.settingsPanel.querySelector("#cfgStable");
      const bufferInput = this.settingsPanel.querySelector("#cfgBuffer");
      preheatInput.value = Math.round((this.config.preheatMs || 0) / 1000);
      stableInput.value = String(this.config.bottomStableThreshold || 12);
      bufferInput.value = String(this.config.bottomThreshold || 600);

      // 绑定变更
      preheatInput.addEventListener("change", () => {
        const seconds = Math.max(0, parseInt(preheatInput.value || "0", 10));
        this.config.preheatMs = seconds * 1000;
        this.saveConfig();
      });
      stableInput.addEventListener("change", () => {
        const count = Math.max(1, parseInt(stableInput.value || "1", 10));
        this.config.bottomStableThreshold = count;
        this.bottomStableThreshold = count;
        this.saveConfig();
      });
      bufferInput.addEventListener("change", () => {
        const px = Math.max(0, parseInt(bufferInput.value || "0", 10));
        this.config.bottomThreshold = px;
        this.bottomThreshold = px;
        this.saveConfig();
      });
    }

    setupEventListeners() {
      this.startBtn.addEventListener("click", () => this.startAutoScroll());
      this.pauseBtn.addEventListener("click", () =>
        this.pauseAutoScroll("manual")
      );
      this.settingsToggleBtn.addEventListener("click", () => {
        const visible = this.settingsPanel.classList.toggle("visible");
        try {
          console.log("AutoScroller: settings", { visible });
        } catch (_) {}
      });
    }

    getViewportHeight() {
      if (this.scrollElement && this.scrollElement !== window) {
        return (
          this.scrollElement.clientHeight || this.scrollElement.offsetHeight
        );
      }
      return window.innerHeight || document.documentElement.clientHeight;
    }

    isAtBottom() {
      const viewportHeight = this.getViewportHeight();
      const currentScroll = this.getScrollTop();
      const totalHeight = this.getScrollHeight();
      const buffer =
        typeof this.bottomThreshold === "number" ? this.bottomThreshold : 0;
      return currentScroll + viewportHeight >= totalHeight - buffer;
    }

    performScroll() {
      const totalHeightNow = this.getScrollHeight();
      if (this.isAtBottom()) {
        // 到达（接近）底部：检查高度是否增长或 DOM 变更
        const now = Date.now();
        const heightGrew = totalHeightNow > this.lastKnownScrollHeight;
        const recentMutation =
          this.lastDomMutationAt && now - this.lastDomMutationAt <= 1500;
        if (heightGrew) {
          this.lastKnownScrollHeight = totalHeightNow;
          this.bottomStableCount = 0;
          this.lastGrowthAt = now;
        } else if (recentMutation) {
          // 近期 DOM 有变更，等待下一次循环
          this.bottomStableCount = 0;
        } else {
          // 页面不可见时，暂停“到末尾”判定，避免后台被站点暂停加载导致误判
          if (this.isPageHidden) return;
          // 刚恢复可见后的预热窗口内，不做“到末尾”判定
          if (this.suppressEndCheckUntil && now < this.suppressEndCheckUntil)
            return;

          this.bottomStableCount += 1;
          const noGrowthMs = this.lastGrowthAt ? now - this.lastGrowthAt : 0;
          // 在真正判定结束前尝试轻推触发加载
          if (
            !this.nudgeInFlight &&
            this.nudgeCount < this.maxNudgesBeforePause
          ) {
            this.nudgeInFlight = true;
            this.nudgeCount += 1;
            try {
              window.scrollBy({ top: 1, behavior: "auto" });
              window.scrollBy({ top: -1, behavior: "auto" });
              console.log("AutoScroller: nudge", {
                nudgeCount: this.nudgeCount,
              });
            } catch (_) {}
            setTimeout(() => (this.nudgeInFlight = false), 300);
          }
          if (
            this.bottomStableCount >= this.bottomStableThreshold &&
            noGrowthMs >= this.noGrowthMsThreshold
          ) {
            this.statusText.textContent = "已到末尾";
            this.pauseAutoScroll(
              `end-of-list: stableCount=${this.bottomStableCount}, noGrowthMs=${noGrowthMs}, scrollHeight=${totalHeightNow}`
            );
          }
        }
        return;
      }

      const currentScroll = this.getScrollTop();
      const targetBottomTop = this.getMaxScrollTop();
      this.doScrollTo(targetBottomTop);

      // 滚动后若高度增长，更新末尾检测计数
      const totalHeightAfter = this.getScrollHeight();
      if (totalHeightAfter > this.lastKnownScrollHeight) {
        this.lastKnownScrollHeight = totalHeightAfter;
        this.bottomStableCount = 0;
      }
    }

    getScrollTop() {
      if (this.scrollElement && this.scrollElement !== window) {
        return this.scrollElement.scrollTop || 0;
      }
      return window.pageYOffset || document.documentElement.scrollTop || 0;
    }

    getScrollHeight() {
      if (this.scrollElement && this.scrollElement !== window) {
        return this.scrollElement.scrollHeight || 0;
      }
      return Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
    }

    getMaxScrollTop() {
      const totalHeight = this.getScrollHeight();
      const viewportHeight = this.getViewportHeight();
      const maxTop = Math.max(0, totalHeight - viewportHeight);
      return maxTop;
    }

    doScrollTo(nextScroll) {
      if (this.scrollElement && this.scrollElement !== window) {
        try {
          this.scrollElement.scrollTo({ top: nextScroll, behavior: "smooth" });
        } catch (_) {
          this.scrollElement.scrollTop = nextScroll;
        }
        return;
      }
      window.scrollTo({ top: nextScroll, behavior: "smooth" });
    }

    detectScrollElement() {
      try {
        // 常见内滚容器选择器（可按需扩展）
        const candidates = [
          ".scroll-container",
          "#scroll-container",
          "main[role='main']",
          "div[style*='overflow: auto']",
          "div[style*='overflow: scroll']",
        ];
        for (const sel of candidates) {
          const el = document.querySelector(sel);
          if (el && el.scrollHeight > el.clientHeight + 100) {
            this.scrollElement = el;
            console.log("AutoScroller: detected scrollElement", sel);
            return;
          }
        }
        // 回退到 window
        this.scrollElement = window;
      } catch (_) {
        this.scrollElement = window;
      }
    }

    startAutoScroll() {
      if (this.isScrolling) return;

      this.isScrolling = true;
      this.statusText.textContent = "滚动中...";
      this.startBtn.disabled = true;
      this.pauseBtn.disabled = false;
      try {
        console.log("AutoScroller: start", { delayMs: this.scrollDelay });
      } catch (_) {}

      // 重置末尾检测
      this.lastKnownScrollHeight = Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      this.bottomStableCount = 0;

      // 立即执行第一次滚动
      this.performScroll();

      // 设置定时器
      this.scrollInterval = setInterval(
        () => this.performScroll(),
        this.scrollDelay
      );

      // 启动worker
      if (this.worker) {
        try {
          console.log("AutoScroller: worker start");
        } catch (_) {}
        this.worker.postMessage({ command: "start" });
      }
    }

    pauseAutoScroll(reason = "unknown") {
      if (!this.isScrolling) return;

      this.isScrolling = false;
      this.statusText.textContent = "暂停中";
      this.startBtn.disabled = false;
      this.pauseBtn.disabled = true;
      try {
        console.warn("AutoScroller: paused", { reason });
      } catch (_) {}

      clearInterval(this.scrollInterval);

      // 暂停worker
      if (this.worker) {
        try {
          console.log("AutoScroller: worker pause", { reason });
        } catch (_) {}
        this.worker.postMessage({ command: "pause" });
      }
    }

    initWorker() {
      if (typeof Worker === "undefined") {
        console.warn("浏览器不支持Web Workers，页面失焦时自动滚动可能不工作");
        return;
      }

      const workerCode = `
                  let scrollTimeout;
                  let isActive = false;

                  self.onmessage = function(e) {
                      if (e.data.command === 'start') {
                          isActive = true;
                          scheduleScroll();
                      } else if (e.data.command === 'pause') {
                          isActive = false;
                          clearTimeout(scrollTimeout);
                      }
                  };

                  function scheduleScroll() {
                      scrollTimeout = setTimeout(() => {
                          if (isActive) {
                              self.postMessage({ action: 'scroll' });
                              scheduleScroll();
                          }
                      }, ${this.scrollDelay});
                  }
              `;

      const blob = new Blob([workerCode], { type: "application/javascript" });
      this.worker = new Worker(URL.createObjectURL(blob));

      this.worker.onmessage = (e) => {
        if (e.data.action === "scroll" && this.isScrolling) {
          this.performScroll();
        }
      };
    }

    initDomObserver() {
      try {
        if (!window.MutationObserver) return;
        const observer = new MutationObserver(() => {
          this.lastDomMutationAt = Date.now();
          const currentHeight = Math.max(
            document.body.scrollHeight,
            document.documentElement.scrollHeight
          );
          if (currentHeight > this.lastKnownScrollHeight) {
            this.lastKnownScrollHeight = currentHeight;
            this.bottomStableCount = 0;
            this.lastGrowthAt = Date.now();
          }
        });
        observer.observe(document.documentElement, {
          childList: true,
          subtree: true,
          attributes: false,
          characterData: false,
        });
        this._domObserver = observer;
      } catch (_) {}
    }

    setupVisibilityHandlers() {
      try {
        document.addEventListener("visibilitychange", () => {
          const now = Date.now();
          if (document.hidden) {
            this.isPageHidden = true;
            try {
              console.log("AutoScroller: page hidden");
            } catch (_) {}
          } else {
            this.isPageHidden = false;
            // 可见后重置末尾相关计数与时间基准
            this.bottomStableCount = 0;
            this.lastGrowthAt = now;
            this.lastDomMutationAt = now;
            // 预热窗口，避免刚恢复就误判
            this.suppressEndCheckUntil = now + (this.config.preheatMs || 0);
            try {
              console.log("AutoScroller: page visible → resume & kick");
            } catch (_) {}
            // 立刻以及数次滚到底并轻推，刺激懒加载
            const kicks = [0, 400, 900, 1500, 2200];
            kicks.forEach((delay) => {
              setTimeout(() => {
                const bottomTop = this.getMaxScrollTop();
                this.doScrollTo(bottomTop);
                try {
                  window.scrollBy({ top: 1, behavior: "auto" });
                  window.scrollBy({ top: -1, behavior: "auto" });
                } catch (_) {}
              }, delay);
            });
          }
        });
      } catch (_) {}
    }
  }

  (function initAutoScroll() {
    function tryInit() {
      try {
        if (!document.body) {
          setTimeout(tryInit, 50);
          return;
        }
        new AutoScroller();
      } catch (e) {
        console.error("AutoScroll初始化失败:", e);
      }
    }
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", tryInit);
    } else {
      setTimeout(tryInit, 0);
    }
  })();
})();
