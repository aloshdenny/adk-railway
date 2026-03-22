import math
from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.5-flash"

# ── Basic Tools ──────────────────────────────────────────
def add(a: float, b: float) -> float:
    """Adds two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts b from a."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Divides a by b."""
    return a / b

# ── Specialist Tools ─────────────────────────────────────
def power(a: float, b: float) -> float:
    """Returns a raised to the power b."""
    return a ** b

def square_root(x: float) -> float:
    """Returns the square root of x."""
    return math.sqrt(x)

def logarithm(x: float, base: float = math.e) -> float:
    """Returns the logarithm of x with the given base (default: natural log)."""
    return math.log(x, base)

def factorial(n: int) -> int:
    """Returns the factorial of n."""
    return math.factorial(n)

def sine(angle_radians: float) -> float:
    """Returns the sine of an angle in radians."""
    return math.sin(angle_radians)

def cosine(angle_radians: float) -> float:
    """Returns the cosine of an angle in radians."""
    return math.cos(angle_radians)

# ── Agents ───────────────────────────────────────────────
calculator_agent = Agent(
    name="calculator_agent",
    model=GEMINI_MODEL,
    description="Handles simple arithmetic: add, subtract, multiply, divide.",
    instruction="You are a simple math assistant. Use the add, subtract, multiply, divide tools to perform basic arithmetic.",
    tools=[add, subtract, multiply, divide],
)

specialist_math_agent = Agent(
    name="specialist_math_agent",
    model=GEMINI_MODEL,
    description="Handles advanced math: power, roots, logarithms, factorials, trigonometry.",
    instruction="You are a specialist math assistant. Use the power, square_root, logarithm, factorial, sine, cosine tools.",
    tools=[power, square_root, logarithm, factorial, sine, cosine],
)

orchestrator = Agent(
    name="orchestrator",
    model=GEMINI_MODEL,
    description="Routes math queries to the correct specialist agent.",
    instruction=(
        "You are an orchestrator for mathematics. "
        "Route to 'calculator_agent' for simple arithmetic, "
        "'specialist_math_agent' for advanced math. "
        "Combine results if both are needed. Never answer directly."
    ),
    sub_agents=[calculator_agent, specialist_math_agent],
)
