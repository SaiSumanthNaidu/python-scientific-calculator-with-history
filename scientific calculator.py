import tkinter as tk
from tkinter import font as tkfont
import math

# ── colour palette ──────────────────────────────────────────────
BG          = "#0d0d0d"
DISPLAY_BG  = "#111111"
DISPLAY_FG  = "#e8e8e8"
EXPR_FG     = "#888888"

BTN_NUM_BG  = "#1e1e1e"
BTN_NUM_FG  = "#e8e8e8"
BTN_NUM_HOV = "#2a2a2a"

BTN_OP_BG   = "#1a1a2e"
BTN_OP_FG   = "#7eb8f7"
BTN_OP_HOV  = "#252545"

BTN_SCI_BG  = "#0f1f0f"
BTN_SCI_FG  = "#6fcf97"
BTN_SCI_HOV = "#1a2e1a"

BTN_EQ_BG   = "#1a3a1a"
BTN_EQ_FG   = "#6fcf97"
BTN_EQ_HOV  = "#22482a"

BTN_CLR_BG  = "#2e1a1a"
BTN_CLR_FG  = "#f47174"
BTN_CLR_HOV = "#3d2222"

BORDER      = "#2a2a2a"
RADIUS      = 8

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.expression = ""
        self.result_shown = False
        self.deg_mode = True          # True = degrees, False = radians
        self.history = []             # Store recent calculations
        self.max_history = 10         # Keep last 10 calculations

        self._build_fonts()
        self._build_display()
        self._build_history()
        self._build_buttons()
        self._bind_keyboard()

    # ── fonts ────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_result = tkfont.Font(family="Courier New", size=32, weight="bold")
        self.f_expr   = tkfont.Font(family="Courier New", size=13)
        self.f_btn    = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.f_sci    = tkfont.Font(family="Courier New", size=11)
        self.f_mode   = tkfont.Font(family="Courier New", size=9)

    # ── display ──────────────────────────────────────────────────
    def _build_display(self):
        frame = tk.Frame(self, bg=DISPLAY_BG, padx=16, pady=12,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=(10, 4))

        self.mode_label = tk.Label(frame, text="DEG", font=self.f_mode,
                                   bg=DISPLAY_BG, fg="#6fcf97", anchor="e")
        self.mode_label.pack(side="top", fill="x")

        self.expr_label = tk.Label(frame, text="", font=self.f_expr,
                                   bg=DISPLAY_BG, fg=EXPR_FG, anchor="e",
                                   height=1, wraplength=360, justify="right")
        self.expr_label.pack(fill="x")

        self.result_label = tk.Label(frame, text="0", font=self.f_result,
                                     bg=DISPLAY_BG, fg=DISPLAY_FG, anchor="e",
                                     height=1)
        self.result_label.pack(fill="x")

    # ── history panel ──────────────────────────────────────────
    def _build_history(self):
        hist_frame = tk.Frame(self, bg=DISPLAY_BG, padx=10, pady=12,
                              highlightbackground=BORDER, highlightthickness=1)
        hist_frame.grid(row=0, column=5, columnspan=2, sticky="nsew", padx=10, pady=(10, 4))
        
        # History title
        title_label = tk.Label(hist_frame, text="History", font=self.f_sci,
                               bg=DISPLAY_BG, fg="#6fcf97")
        title_label.pack(fill="x", pady=(0, 8))
        
        # Scrollable history frame
        scroll_frame = tk.Frame(hist_frame, bg=DISPLAY_BG)
        scroll_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame, bg=BORDER, troughcolor=DISPLAY_BG)
        scrollbar.pack(side="right", fill="y")
        
        self.history_text = tk.Text(scroll_frame, height=10, width=18,
                                    font=tkfont.Font(family="Courier New", size=9),
                                    bg="#0a0a0a", fg="#b0b0b0",
                                    yscrollcommand=scrollbar.set,
                                    relief="flat", padx=4, pady=4,
                                    state="disabled",
                                    wrap="word",
                                    highlightthickness=0)
        self.history_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Clear history button
        clear_hist_btn = tk.Label(hist_frame, text="Clear", font=self.f_sci,
                                  bg=BTN_CLR_BG, fg=BTN_CLR_FG, cursor="hand2",
                                  relief="flat", padx=4, pady=4,
                                  highlightbackground=BORDER, highlightthickness=1)
        clear_hist_btn.pack(fill="x", pady=(8, 0))
        clear_hist_btn.bind("<Button-1>", lambda e: self._clear_history())
        clear_hist_btn.bind("<Enter>", lambda e: clear_hist_btn.config(bg=BTN_CLR_HOV))
        clear_hist_btn.bind("<Leave>", lambda e: clear_hist_btn.config(bg=BTN_CLR_BG))

    # ── button grid ──────────────────────────────────────────────
    def _build_buttons(self):
        pad = {"padx": 4, "pady": 4}

        # row, col, text, action, style
        layout = [
            # row 1 – scientific top
            (1,0,"sin",  lambda: self._sci("sin"),  "sci"),
            (1,1,"cos",  lambda: self._sci("cos"),  "sci"),
            (1,2,"tan",  lambda: self._sci("tan"),  "sci"),
            (1,3,"log",  lambda: self._sci("log"),  "sci"),
            (1,4,"ln",   lambda: self._sci("ln"),   "sci"),
            (1,5,"π",    lambda: self._append("math.pi"), "sci"),
            (1,6,"e",    lambda: self._append("math.e"),  "sci"),

            # row 2 – scientific bottom
            (2,0,"x²",   lambda: self._append("**2"),       "sci"),
            (2,1,"x³",   lambda: self._append("**3"),       "sci"),
            (2,2,"xʸ",   lambda: self._append("**"),        "sci"),
            (2,3,"√",    lambda: self._sci("sqrt"),         "sci"),
            (2,4,"∛",    lambda: self._sci("cbrt"),         "sci"),
            (2,5,"1/x",  lambda: self._append("**-1"),      "sci"),
            (2,6,"DEG",  self._toggle_mode,                  "sci"),

            # row 3 – clear / brackets / percent
            (3,0,"C",    self._clear,          "clr"),
            (3,1,"CE",   self._ce,             "clr"),
            (3,2,"(",    lambda: self._append("("), "op"),
            (3,3,")",    lambda: self._append(")"), "op"),
            (3,4,"%",    lambda: self._append("%"),  "op"),
            (3,5,"⌫",    self._backspace,       "clr"),
            (3,6,"±",    self._negate,          "op"),

            # rows 4-6 – digits + operators
            (4,0,"7",    lambda: self._append("7"), "num"),
            (4,1,"8",    lambda: self._append("8"), "num"),
            (4,2,"9",    lambda: self._append("9"), "num"),
            (4,3,"÷",    lambda: self._append("/"), "op"),
            (4,4,"EXP",  lambda: self._append("e"), "sci"),
            (4,5,"(",    lambda: self._append("("), "op"),
            (4,6,")",    lambda: self._append(")"), "op"),

            (5,0,"4",    lambda: self._append("4"), "num"),
            (5,1,"5",    lambda: self._append("5"), "num"),
            (5,2,"6",    lambda: self._append("6"), "num"),
            (5,3,"×",    lambda: self._append("*"), "op"),
            (5,4,"abs",  lambda: self._sci("abs"),  "sci"),
            (5,5,"n!",   lambda: self._sci("fact"), "sci"),
            (5,6,"mod",  lambda: self._append("%"), "op"),

            (6,0,"1",    lambda: self._append("1"), "num"),
            (6,1,"2",    lambda: self._append("2"), "num"),
            (6,2,"3",    lambda: self._append("3"), "num"),
            (6,3,"−",    lambda: self._append("-"), "op"),
            (6,4,"sin⁻¹",lambda: self._sci("asin"), "sci"),
            (6,5,"cos⁻¹",lambda: self._sci("acos"), "sci"),
            (6,6,"tan⁻¹",lambda: self._sci("atan"), "sci"),

            (7,0,"0",    lambda: self._append("0"), "num"),
            (7,1,".",    lambda: self._append("."), "num"),
            (7,2,"00",   lambda: self._append("00"),"num"),
            (7,3,"+",    lambda: self._append("+"), "op"),
        ]

        styles = {
            "num": (BTN_NUM_BG, BTN_NUM_FG, BTN_NUM_HOV, self.f_btn),
            "op":  (BTN_OP_BG,  BTN_OP_FG,  BTN_OP_HOV,  self.f_btn),
            "sci": (BTN_SCI_BG, BTN_SCI_FG, BTN_SCI_HOV, self.f_sci),
            "clr": (BTN_CLR_BG, BTN_CLR_FG, BTN_CLR_HOV, self.f_btn),
            "eq":  (BTN_EQ_BG,  BTN_EQ_FG,  BTN_EQ_HOV,  self.f_btn),
        }

        container = tk.Frame(self, bg=BG)
        container.grid(row=1, column=0, padx=10, pady=4, sticky="nsew")

        for r, c, text, cmd, style in layout:
            bg, fg, hov, fnt = styles[style]
            self._make_btn(container, text, cmd, r-1, c, bg, fg, hov, fnt, **pad)

        # "=" spans columns 4-6 on last row
        bg, fg, hov, fnt = styles["eq"]
        eq_btn = self._make_btn(container, "=", self._evaluate,
                                6, 4, bg, fg, hov, fnt,
                                padx=4, pady=4, colspan=3)

    # ── history management ──────────────────────────────────────
    def _add_to_history(self, expression, result):
        """Add calculation to history."""
        self.history.append((expression, result))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self._update_history_display()
    
    def _update_history_display(self):
        """Update the history text widget."""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        for expr, result in reversed(self.history):
            # Format: expression = result
            line = f"{expr} = {result}\n"
            self.history_text.insert("end", line)
        self.history_text.config(state="disabled")
        self.history_text.see("end")  # Scroll to bottom
    
    def _clear_history(self):
        """Clear all history."""
        self.history = []
        self._update_history_display()

    def _make_btn(self, parent, text, cmd, row, col,
                  bg, fg, hov, fnt, padx=4, pady=4, colspan=1):
        btn = tk.Label(parent, text=text, font=fnt,
                       bg=bg, fg=fg, cursor="hand2",
                       relief="flat", padx=6, pady=10,
                       highlightbackground=BORDER,
                       highlightthickness=1)
        btn.grid(row=row, column=col, columnspan=colspan,
                 padx=padx, pady=pady, sticky="nsew",
                 ipadx=4, ipady=4)
        parent.columnconfigure(col, weight=1)
        parent.rowconfigure(row, weight=1)

        btn.bind("<Button-1>",  lambda e: cmd())
        btn.bind("<Enter>",     lambda e: btn.config(bg=hov))
        btn.bind("<Leave>",     lambda e: btn.config(bg=bg))
        return btn

    # ── keyboard binding ─────────────────────────────────────────
    def _bind_keyboard(self):
        self.bind("<Key>", self._on_key)

    def _on_key(self, event):
        k = event.keysym
        ch = event.char
        if ch in "0123456789.+-*/()%": self._append(ch)
        elif k == "Return":            self._evaluate()
        elif k == "BackSpace":         self._backspace()
        elif k == "Escape":            self._clear()

    # ── state helpers ─────────────────────────────────────────────
    def _append(self, val):
        if self.result_shown and val not in "+-*/%()**":
            self.expression = ""
        self.result_shown = False
        self.expression += str(val)
        self._update_display(self.expression)

    def _update_display(self, value, expr=""):
        display = (value
                   .replace("math.pi", "π")
                   .replace("math.e", "e")
                   .replace("math.sin(", "sin(")
                   .replace("math.cos(", "cos(")
                   .replace("math.tan(", "tan(")
                   .replace("math.log10(", "log(")
                   .replace("math.log(", "ln(")
                   .replace("math.sqrt(", "√(")
                   .replace("math.fabs(", "abs(")
                   .replace("math.factorial(", "n!(")
                   .replace("math.asin(", "sin⁻¹(")
                   .replace("math.acos(", "cos⁻¹(")
                   .replace("math.atan(", "tan⁻¹("))
        if expr:
            self.expr_label.config(text=expr)
            self.result_label.config(text=display)
        else:
            self.result_label.config(text=display or "0")

    # ── scientific helpers ────────────────────────────────────────
    def _sci(self, fn):
        if self.result_shown and self.expression:
            val = self.expression
        else:
            val = ""

        if fn == "sin":
            if self.deg_mode and val:
                self.expression = f"math.sin(math.radians({val}))"
            else:
                self.expression = f"math.sin({val}"
        elif fn == "cos":
            if self.deg_mode and val:
                self.expression = f"math.cos(math.radians({val}))"
            else:
                self.expression = f"math.cos({val}"
        elif fn == "tan":
            if self.deg_mode and val:
                self.expression = f"math.tan(math.radians({val}))"
            else:
                self.expression = f"math.tan({val}"
        elif fn == "asin":
            self.expression = f"math.degrees(math.asin({val}))" if self.deg_mode else f"math.asin({val}"
        elif fn == "acos":
            self.expression = f"math.degrees(math.acos({val}))" if self.deg_mode else f"math.acos({val}"
        elif fn == "atan":
            self.expression = f"math.degrees(math.atan({val}))" if self.deg_mode else f"math.atan({val}"
        elif fn == "log":
            self.expression = f"math.log10({val}"
        elif fn == "ln":
            self.expression = f"math.log({val}"
        elif fn == "sqrt":
            self.expression = f"math.sqrt({val}"
        elif fn == "cbrt":
            self.expression = f"({val})**(1/3)" if val else f"**(1/3)"
        elif fn == "abs":
            self.expression = f"math.fabs({val}"
        elif fn == "fact":
            self.expression = f"math.factorial(int({val}))" if val else "math.factorial(int("

        self.result_shown = False
        self._update_display(self.expression)

    def _toggle_mode(self):
        self.deg_mode = not self.deg_mode
        mode = "DEG" if self.deg_mode else "RAD"
        self.mode_label.config(text=mode)

    def _negate(self):
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self._update_display(self.expression)

    def _clear(self):
        self.expression = ""
        self.result_shown = False
        self.expr_label.config(text="")
        self.result_label.config(text="0")

    def _ce(self):
        """Clear last entry."""
        # Remove last token (number or operator)
        import re
        self.expression = re.sub(r'[\d.]+$|[+\-*/%^()]$', '', self.expression)
        self._update_display(self.expression or "0")

    def _backspace(self):
        self.expression = self.expression[:-1]
        self._update_display(self.expression or "0")

    # ── evaluate ─────────────────────────────────────────────────
    def _evaluate(self):
        if not self.expression:
            return
        expr_display = self.expression
        try:
            result = eval(self.expression, {"__builtins__": {}}, {"math": math})
            # Clean up float display
            if isinstance(result, float) and result.is_integer():
                result_str = str(int(result))
            else:
                result_str = f"{result:.10g}"
            self.expression = result_str
            self.result_shown = True
            self._update_display(result_str, expr=expr_display + " =")
            # Add to history
            self._add_to_history(expr_display, result_str)
        except ZeroDivisionError:
            self.result_label.config(text="÷ 0 Error", fg=BTN_CLR_FG)
            self.expression = ""
        except Exception:
            self.result_label.config(text="Error", fg=BTN_CLR_FG)
            self.expression = ""


if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
