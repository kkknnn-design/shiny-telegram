import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import winsound
import threading

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
LONG_BREAK_INTERVAL = 4  # long break after every 4 work sessions

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("番茄钟")
        self.root.geometry("360x440")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.root.attributes("-topmost", True)

        self.seconds_left = WORK_MIN * 60
        self.running = False
        self.work_mode = True
        self.session_count = 0
        self.after_id = None

        self._build_ui()
        self._update_display()

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.font_timer = ("Segoe UI", 64, "bold")
        self.font_label = ("Segoe UI", 12)
        self.font_btn   = ("Segoe UI", 10)

        main = tk.Frame(self.root, bg="#1e1e2e")
        main.pack(expand=True, fill="both", padx=24, pady=24)

        self.mode_var = tk.StringVar(value="🍅 工作时间")
        tk.Label(
            main, textvariable=self.mode_var, font=self.font_label,
            bg="#1e1e2e", fg="#cdd6f4"
        ).pack(pady=(0, 8))

        self.canvas = tk.Canvas(
            main, width=260, height=260, bg="#1e1e2e",
            highlightthickness=0
        )
        self.canvas.pack(pady=(0, 8))

        self._draw_ring(0)

        self.timer_var = tk.StringVar(value="25:00")
        self.canvas.create_text(
            130, 117, text="25:00", font=self.font_timer,
            fill="#cdd6f4", tags="timer_text"
        )

        self.progress = ttk.Progressbar(
            main, length=310, mode="determinate", maximum=WORK_MIN * 60
        )
        self.progress.pack(pady=(0, 6))

        self.session_var = tk.StringVar(value="已完成: 0 个番茄")
        tk.Label(
            main, textvariable=self.session_var, font=self.font_label,
            bg="#1e1e2e", fg="#a6adc8"
        ).pack(pady=(0, 12))

        btn_frame = tk.Frame(main, bg="#1e1e2e")
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, text="▶  开始", command=self.start,
            font=self.font_btn, bg="#a6e3a1", fg="#1e1e2e",
            activebackground="#94d89d", activeforeground="#1e1e2e",
            relief="flat", padx=16, pady=6, bd=0, cursor="hand2"
        )
        self.start_btn.pack(side="left", padx=4)

        self.pause_btn = tk.Button(
            btn_frame, text="⏸  暂停", command=self.pause,
            font=self.font_btn, bg="#f9e2af", fg="#1e1e2e",
            activebackground="#f1d88a", activeforeground="#1e1e2e",
            relief="flat", padx=16, pady=6, bd=0, cursor="hand2"
        )
        self.pause_btn.pack(side="left", padx=4)

        self.reset_btn = tk.Button(
            btn_frame, text="↺  重置", command=self.reset,
            font=self.font_btn, bg="#f38ba8", fg="#1e1e2e",
            activebackground="#ed7590", activeforeground="#1e1e2e",
            relief="flat", padx=16, pady=6, bd=0, cursor="hand2"
        )
        self.reset_btn.pack(side="left", padx=4)

        bottom = tk.Frame(main, bg="#1e1e2e")
        bottom.pack(pady=(10, 0))

        self.topmost_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            bottom, text="置顶窗口", variable=self.topmost_var,
            command=self._toggle_topmost,
            bg="#1e1e2e", fg="#a6adc8", selectcolor="#1e1e2e",
            activebackground="#1e1e2e", activeforeground="#cdd6f4",
            font=self.font_label
        ).pack(side="left", padx=12)

        self.skip_btn = tk.Button(
            bottom, text="跳过 →", command=self.skip,
            font=self.font_label, bg="#45475a", fg="#cdd6f4",
            activebackground="#585b70", activeforeground="#cdd6f4",
            relief="flat", padx=12, pady=4, bd=0, cursor="hand2"
        )
        self.skip_btn.pack(side="left", padx=12)

    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def _draw_ring(self, fraction):
        self.canvas.delete("ring")
        x0, y0, x1, y1 = 20, 20, 240, 240
        extent = 360 * fraction
        color = "#cba6f7" if self.work_mode else "#a6e3a1"
        if extent > 0:
            self.canvas.create_arc(
                x0, y0, x1, y1, start=90, extent=-extent,
                outline=color, width=8, style="arc", tags="ring"
            )
        # background ring
        self.canvas.create_arc(
            x0, y0, x1, y1, start=90, extent=-360,
            outline="#313244", width=8, style="arc", tags="ring"
        )

    def _update_display(self):
        m, s = divmod(self.seconds_left, 60)
        self.timer_var.set(f"{m:02d}:{s:02d}")
        self.canvas.itemconfigure("timer_text", text=self.timer_var.get())

        total = (WORK_MIN if self.work_mode else self._break_minutes()) * 60
        elapsed = total - self.seconds_left
        self.progress["value"] = elapsed
        self.progress["maximum"] = total

        fraction = elapsed / total if total > 0 else 0
        self._draw_ring(fraction)

    def _break_minutes(self):
        return LONG_BREAK_MIN if self.session_count > 0 and self.session_count % LONG_BREAK_INTERVAL == 0 else SHORT_BREAK_MIN

    def _tick(self):
        if not self.running:
            return
        if self.seconds_left > 0:
            self.seconds_left -= 1
            self._update_display()
            self.after_id = self.root.after(1000, self._tick)
        else:
            self._finish_phase()

    def _finish_phase(self):
        self.running = False
        self.after_id = None

        if self.work_mode:
            self.session_count += 1
            self.session_var.set(f"已完成: {self.session_count} 个番茄")
            self._alert("🍅 时间到！该休息一下了。")

            if self.session_count % LONG_BREAK_INTERVAL == 0:
                self.seconds_left = LONG_BREAK_MIN * 60
                self.mode_var.set("☕ 长休息")
            else:
                self.seconds_left = SHORT_BREAK_MIN * 60
                self.mode_var.set("☕ 短休息")
            self.work_mode = False
        else:
            self._alert("⏰ 休息结束！继续工作吧。")
            self.seconds_left = WORK_MIN * 60
            self.mode_var.set("🍅 工作时间")
            self.work_mode = True

        self._update_display()
        self.start_btn.configure(text="▶  开始")
        self._update_skip_state()

    def _alert(self, msg):
        threading.Thread(target=self._beep_sequence, daemon=True).start()
        self.root.after(100, lambda: messagebox.showinfo("番茄钟提醒", msg))

    def _beep_sequence(self):
        freq = 880 if self.work_mode else 660
        for _ in range(3):
            winsound.Beep(freq, 300)
            winsound.Beep(freq // 2, 500)

    def _update_skip_state(self):
        if self.running:
            self.skip_btn.configure(state="normal", bg="#45475a", fg="#cdd6f4")
        else:
            self.skip_btn.configure(state="disabled", bg="#313244", fg="#6c7086")

    def start(self):
        if not self.running:
            self.running = True
            self.start_btn.configure(text="⏸ 运行中...")
            self._update_skip_state()
            self.after_id = self.root.after(1000, self._tick)

    def _cancel_timer(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_btn.configure(text="▶  开始")
        self._update_skip_state()

    def pause(self):
        if self.running:
            self._cancel_timer()

    def reset(self):
        self._cancel_timer()
        self.work_mode = True
        self.seconds_left = WORK_MIN * 60
        self.mode_var.set("🍅 工作时间")
        self._update_display()

    def skip(self):
        if self.running:
            self._cancel_timer()
        self._finish_phase()


def main():
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
