// Note: Backend data handling uses Polars. In-browser Python runs in Pyodide,
// where Polars is not available; we use pandas here only for user code execution.
let pyodideReadyPromise;

async function ensurePyodide() {
  if (!pyodideReadyPromise) {
    pyodideReadyPromise = (async () => {
      self.pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/" });
      await pyodide.loadPackage(["pandas"]);
      return self.pyodide;
    })();
  }
  return pyodideReadyPromise;
}

// Runs user code with a pandas DataFrame named `df` built from sampleRows (array of objects).
// The user must set `out` to either a pandas DataFrame or a Plotly figure dict.
// Also captures stdout/stderr and returns them.
export async function runPython(code, sampleRows) {
  const py = await ensurePyodide();
  const rt = self.pyodide;

  // Capture stdout/stderr
  const stdoutChunks = [];
  const stderrChunks = [];
  const restoreStdout = rt.setStdout({ batched: (s) => stdoutChunks.push(s) });
  const restoreStderr = rt.setStderr({ batched: (s) => stderrChunks.push(s) });

  try {
    // Deep-convert JS -> Python to avoid pandas dtype errors
    const pyInput = py.toPy(sampleRows);
    py.globals.set("input_data", pyInput);
    try { pyInput.destroy && pyInput.destroy(); } catch (_) {}

    const bootstrap = `
import pandas as pd
import json
out = None
# Build DataFrame robustly from list-of-dicts
try:
    df = pd.DataFrame.from_records(input_data)
except Exception:
    # Force pure-Python primitives via JSON round-trip
    df = pd.DataFrame.from_records(json.loads(json.dumps(input_data)))
del input_data
`;
    await py.runPythonAsync(bootstrap + "\n" + code + "\n");

    // Normalize Series -> DataFrame for consistent handling
    try {
      await py.runPythonAsync(`
import pandas as pd
if isinstance(out, pd.Series):
    out = out.to_frame()
`);
    } catch (_) {}

    const outObj = py.globals.get("out");
    if (outObj === undefined || outObj === null) {
      return {
        kind: "none",
        data: null,
        error: "No variable 'out' set by code.",
        stdout: stdoutChunks.join(""),
        stderr: stderrChunks.join("")
      };
    }

    // Determine output type robustly
    const isDf = await py.runPythonAsync(`import pandas as pd\nisinstance(out, pd.DataFrame)`);
    if (isDf) {
      // Convert DataFrame -> records and then to plain JS
      const rowsPy = await py.runPythonAsync("out.to_dict(orient='records')");
      const rowsJs = rowsPy.toJs({ dict_converter: Object.fromEntries });
      try { rowsPy.destroy && rowsPy.destroy(); } catch (_) {}
      try { outObj.destroy && outObj.destroy(); } catch (_) {}
      return {
        kind: "frame",
        data: rowsJs,
        error: null,
        stdout: stdoutChunks.join(""),
        stderr: stderrChunks.join("")
      };
    }

    // Plotly-like outputs: Figure or dict or list-of-traces
    const hasToPlotly = await py.runPythonAsync("hasattr(out, 'to_plotly_json')");
    const hasToDict = await py.runPythonAsync("hasattr(out, 'to_dict')");
    const isDict = await py.runPythonAsync("isinstance(out, dict)");
    let figJs = null;

    try {
      if (hasToPlotly) {
        const figPy = await py.runPythonAsync("out.to_plotly_json()");
        figJs = figPy.toJs({ dict_converter: Object.fromEntries });
        try { figPy.destroy && figPy.destroy(); } catch (_) {}
      } else if (isDict) {
        figJs = outObj.toJs({ dict_converter: Object.fromEntries });
      } else if (hasToDict) {
        const figPy = await py.runPythonAsync("out.to_dict()");
        figJs = figPy.toJs({ dict_converter: Object.fromEntries });
        try { figPy.destroy && figPy.destroy(); } catch (_) {}
      } else {
        // Generic conversion fallback
        figJs = outObj.toJs({ dict_converter: Object.fromEntries });
      }
    } catch (e) {
      // Final fallback: generic conversion
      figJs = outObj.toJs({ dict_converter: Object.fromEntries });
    } finally {
      try { outObj.destroy && outObj.destroy(); } catch (_) {}
    }

    return {
      kind: "plotly",
      data: figJs,
      error: null,
      stdout: stdoutChunks.join(""),
      stderr: stderrChunks.join("")
    };
  } catch (e) {
    return {
      kind: "error",
      data: null,
      error: String(e),
      stdout: stdoutChunks.join(""),
      stderr: stderrChunks.join("")
    };
  } finally {
    try { restoreStdout(); } catch (_) {}
    try { restoreStderr(); } catch (_) {}
  }
}
