/* AI-901 quiz portal — exam engine
 * Banks register themselves in window.BANKS = { id: {title, minutes, questions:[{q,o,a,d,x}]} }
 *   q = question text · o = options · a = index of correct option
 *   d = difficulty 1 easy / 2 moderate / 3 hard · x = explanation
 */
window.BANKS = window.BANKS || {};

(function () {
  "use strict";

  let exam = null;   // active exam state
  let timerId = null;

  const $ = (sel) => document.querySelector(sel);

  // ---------- utilities ----------------------------------------------------
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function fmt(sec) {
    const m = Math.floor(sec / 60), s = sec % 60;
    return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
  }

  function esc(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  const DIFF = { 1: ["d1", "Easy"], 2: ["d2", "Moderate"], 3: ["d3", "Hard"] };
  const LETTERS = "ABCDE";

  // ---------- portal (home) ------------------------------------------------
  function renderHome() {
    document.querySelectorAll("[data-bank]").forEach((card) => {
      const id = card.getAttribute("data-bank");
      const bank = window.BANKS[id];
      const meta = card.querySelector(".meta");
      const btn = card.querySelector("button");
      if (!bank) {
        if (meta) meta.textContent = "Bank failed to load";
        if (btn) btn.disabled = true;
        return;
      }
      if (meta) meta.textContent =
        bank.questions.length + " questions · " + bank.minutes + " min · pass 70%";
      const best = localStorage.getItem("ai901.best." + id);
      const bestEl = card.querySelector(".best");
      if (bestEl && best) bestEl.textContent = "Best score: " + best + "%";
      if (btn) btn.onclick = () => showStart(id);
    });
  }

  // ---------- start screen -------------------------------------------------
  function showStart(id) {
    const bank = window.BANKS[id];
    $("#homeView").style.display = "none";
    $("#examView").style.display = "block";
    $("#examView").innerHTML =
      '<div class="panel">' +
      "<h2>" + esc(bank.title) + "</h2>" +
      "<p><b>" + bank.questions.length + " questions · " + bank.minutes +
      " minutes · passing score 70%</b></p>" +
      "<ul>" +
      "<li>The timer starts the moment you press <b>Start exam</b> and cannot be paused.</li>" +
      "<li>Each question has exactly <b>one</b> correct answer.</li>" +
      "<li>You can move back and forth, and flag questions for review.</li>" +
      "<li>The exam auto-submits when time runs out.</li>" +
      "<li>After submitting you enter <b>review mode</b>: every question shows the correct answer, " +
      "your answer, and a full explanation — just like the official practice experience.</li>" +
      "</ul>" +
      '<div class="qnav"><button class="primary" id="startBtn">Start exam ▶</button>' +
      '<button id="backBtn">← Back to portal</button></div></div>';
    $("#startBtn").onclick = () => startExam(id);
    $("#backBtn").onclick = goHome;
    window.scrollTo(0, 0);
  }

  function goHome() {
    if (timerId) clearInterval(timerId);
    exam = null;
    $("#examView").style.display = "none";
    $("#homeView").style.display = "block";
    renderHome();
    window.scrollTo(0, 0);
  }

  // ---------- exam ----------------------------------------------------------
  function startExam(id) {
    const bank = window.BANKS[id];
    // shuffle question order and each question's options
    const qs = shuffle(bank.questions).map((src) => {
      const order = shuffle(src.o.map((_, i) => i));
      return {
        q: src.q, d: src.d || 2, x: src.x,
        o: order.map((i) => src.o[i]),
        a: order.indexOf(src.a),
        sel: null, flag: false,
      };
    });
    exam = { id, bank, qs, cur: 0, left: bank.minutes * 60, done: false };
    buildExamShell();
    renderQuestion();
    timerId = setInterval(tick, 1000);
  }

  function tick() {
    exam.left--;
    const t = $("#timer");
    if (t) {
      t.textContent = fmt(Math.max(exam.left, 0));
      t.classList.toggle("low", exam.left <= 120);
    }
    if (exam.left <= 0) {
      clearInterval(timerId);
      submitExam(true);
    }
  }

  function buildExamShell() {
    $("#examView").innerHTML =
      '<div class="exambar">' +
      '<span class="title">' + esc(exam.bank.title) + "</span>" +
      '<span class="progress" id="prog"></span>' +
      '<span class="timer" id="timer">' + fmt(exam.left) + "</span></div>" +
      '<div class="examlayout">' +
      '<div class="qcard" id="qcard"></div>' +
      '<div class="palette"><h4>Questions</h4><div class="pgrid" id="pgrid"></div>' +
      '<div class="legend">' +
      '<span class="dot" style="background:#e8f1fb;border:1px solid #0b5cab"></span>Answered<br>' +
      '<span class="dot" style="background:#fff4d6;border:1px solid #9a6a00"></span>Flagged<br>' +
      '<span class="dot" style="background:#fff;border:1px solid #d5e2ef"></span>Unseen / blank' +
      "</div></div></div>";
    const pg = $("#pgrid");
    exam.qs.forEach((_, i) => {
      const b = document.createElement("button");
      b.textContent = i + 1;
      b.onclick = () => { exam.cur = i; renderQuestion(); };
      pg.appendChild(b);
    });
  }

  function paintPalette() {
    const btns = $("#pgrid").children;
    exam.qs.forEach((q, i) => {
      const b = btns[i];
      b.className = "";
      if (exam.done) {
        b.classList.add(q.sel === q.a ? "rok" : "rbad");
      } else {
        if (q.sel !== null) b.classList.add("answered");
        if (q.flag) b.classList.add("flag");
      }
      if (i === exam.cur) b.classList.add("cur");
    });
    const answered = exam.qs.filter((q) => q.sel !== null).length;
    $("#prog").textContent = exam.done
      ? "Review mode"
      : answered + " / " + exam.qs.length + " answered";
  }

  function renderQuestion() {
    const q = exam.qs[exam.cur];
    const n = exam.cur + 1, total = exam.qs.length;
    const [dc, dl] = DIFF[q.d] || DIFF[2];
    let h =
      '<div class="qtop"><span class="qnum">QUESTION ' + n + " OF " + total +
      '</span><span class="qdiff ' + dc + '">' + dl + "</span></div>" +
      '<div class="qtext">' + esc(q.q) + "</div>";

    q.o.forEach((opt, i) => {
      let cls = "opt";
      if (exam.done) {
        if (i === q.a) cls += " correct";
        else if (i === q.sel) cls += " wrong";
      } else if (i === q.sel) cls += " sel";
      h += '<div class="' + cls + '" data-i="' + i + '">' +
        '<span class="letter">' + LETTERS[i] + "</span><span>" + esc(opt) + "</span></div>";
    });

    if (exam.done) {
      const ok = q.sel === q.a;
      h += '<div class="verdict ' + (ok ? "ok" : "bad") + '">' +
        (q.sel === null
          ? "✖ Not answered — correct answer: " + LETTERS[q.a]
          : ok ? "✔ Correct" : "✖ Incorrect — you chose " + LETTERS[q.sel] +
            ", correct answer is " + LETTERS[q.a]) + "</div>";
      h += '<div class="explain"><b>Explanation:</b> ' + esc(q.x) + "</div>";
    }

    h += '<div class="qnav">' +
      '<button id="prevB"' + (exam.cur === 0 ? " disabled" : "") + ">← Previous</button>" +
      '<button id="nextB" class="primary"' + (exam.cur === total - 1 ? " disabled" : "") + ">Next →</button>";
    if (!exam.done) {
      h += '<button id="flagB" class="flagbtn' + (q.flag ? " flagged" : "") + '">' +
        (q.flag ? "⚑ Flagged" : "⚑ Flag") + "</button>" +
        '<button id="submitB" class="submit">Submit exam</button>';
    } else {
      h += '<button id="homeB" class="submit">Finish review</button>';
    }
    h += "</div>";

    $("#qcard").innerHTML = h;

    if (!exam.done) {
      document.querySelectorAll("#qcard .opt").forEach((el) => {
        el.onclick = () => {
          q.sel = parseInt(el.getAttribute("data-i"), 10);
          renderQuestion();
        };
      });
      $("#flagB").onclick = () => { q.flag = !q.flag; renderQuestion(); };
      $("#submitB").onclick = () => confirmSubmit();
    } else {
      $("#homeB").onclick = () => showResult();
    }
    $("#prevB").onclick = () => { exam.cur--; renderQuestion(); };
    $("#nextB").onclick = () => { exam.cur++; renderQuestion(); };
    paintPalette();
    window.scrollTo(0, 0);
  }

  function confirmSubmit() {
    const blank = exam.qs.filter((q) => q.sel === null).length;
    const msg = blank
      ? "You still have " + blank + " unanswered question(s). Submit anyway?"
      : "Submit the exam now?";
    if (window.confirm(msg)) submitExam(false);
  }

  function submitExam(auto) {
    if (timerId) clearInterval(timerId);
    exam.done = true;
    exam.auto = auto;
    showResult();
  }

  // ---------- results --------------------------------------------------------
  function showResult() {
    const total = exam.qs.length;
    const right = exam.qs.filter((q) => q.sel === q.a).length;
    const pct = Math.round((right / total) * 100);
    const pass = pct >= 70;
    // per-difficulty breakdown
    const bd = { 1: [0, 0], 2: [0, 0], 3: [0, 0] };
    exam.qs.forEach((q) => {
      bd[q.d][1]++;
      if (q.sel === q.a) bd[q.d][0]++;
    });
    const best = parseInt(localStorage.getItem("ai901.best." + exam.id) || "0", 10);
    if (pct > best) localStorage.setItem("ai901.best." + exam.id, String(pct));

    // stash the exam shell so "review answers" can rebuild it
    $("#examView").innerHTML =
      '<div class="panel" style="text-align:center">' +
      "<h2>" + esc(exam.bank.title) + " — result</h2>" +
      (exam.auto ? '<p style="color:#c42b1c;font-weight:600">⏰ Time expired — the exam was submitted automatically.</p>' : "") +
      '<div class="scorebig ' + (pass ? "pass" : "fail") + '">' + pct + "%</div>" +
      '<span class="badge ' + (pass ? "pass" : "fail") + '">' +
      (pass ? "PASS — 70% required" : "FAIL — 70% required") + "</span>" +
      '<div class="statrow">' +
      '<div class="stat"><div class="v">' + right + " / " + total + '</div><div class="k">Correct</div></div>' +
      '<div class="stat"><div class="v">' + bd[1][0] + "/" + bd[1][1] + '</div><div class="k">Easy</div></div>' +
      '<div class="stat"><div class="v">' + bd[2][0] + "/" + bd[2][1] + '</div><div class="k">Moderate</div></div>' +
      '<div class="stat"><div class="v">' + bd[3][0] + "/" + bd[3][1] + '</div><div class="k">Hard</div></div>' +
      "</div>" +
      '<div class="qnav" style="justify-content:center">' +
      '<button id="reviewB" class="primary">Review answers & explanations</button>' +
      '<button id="retakeB">Retake</button>' +
      '<button id="homeB2">Back to portal</button></div></div>';

    $("#reviewB").onclick = () => {
      exam.cur = 0;
      buildExamShell();
      $("#timer").textContent = "REVIEW";
      renderQuestion();
    };
    $("#retakeB").onclick = () => startExam(exam.id);
    $("#homeB2").onclick = goHome;
    window.scrollTo(0, 0);
  }

  document.addEventListener("DOMContentLoaded", renderHome);
})();
