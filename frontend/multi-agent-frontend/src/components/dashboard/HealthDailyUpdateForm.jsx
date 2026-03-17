import { useState } from "react";
import { HealthDailyUpdate } from "../../services/api";
import toast from "react-hot-toast";

// // ── config ────────────────────────────────────────────────────────────────────
// const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const METRICS = [
  {
    field: "heart_rate",
    label: "Heart rate",
    unit: "bpm",
    icon: "♥",
    min: 30,
    max: 220,
    normalMin: 60,
    normalMax: 100,
    placeholder: "72",
    color: "#e05252",
  },
  {
    field: "spo2",
    label: "SpO₂",
    unit: "%",
    icon: "◎",
    min: 70,
    max: 100,
    normalMin: 95,
    normalMax: 100,
    placeholder: "98",
    color: "#4f8ef7",
  },
  {
    field: "bp_systolic",
    label: "Systolic BP",
    unit: "mmHg",
    icon: "↑",
    min: 70,
    max: 220,
    normalMin: 90,
    normalMax: 120,
    placeholder: "120",
    color: "#f7a94f",
  },
  {
    field: "bp_diastolic",
    label: "Diastolic BP",
    unit: "mmHg",
    icon: "↓",
    min: 40,
    max: 140,
    normalMin: 60,
    normalMax: 80,
    placeholder: "80",
    color: "#f7a94f",
  },
];

// ── helpers ───────────────────────────────────────────────────────────────────
function getStatus(metric, raw) {
  if (raw === "" || raw === null || raw === undefined) return "empty";
  const v = parseInt(raw, 10);
  if (isNaN(v) || v < metric.min || v > metric.max) return "critical";
  if (v >= metric.normalMin && v <= metric.normalMax) return "normal";
  return "elevated";
}

const STATUS_META = {
  empty: { label: "", bg: "transparent", text: "#888", ring: "#d0d0d0" },
  normal: { label: "Normal", bg: "#e8f7ef", text: "#1d7a4a", ring: "#4caf80" },
  elevated: { label: "Elevated", bg: "#fff8e8", text: "#b46800", ring: "#f7c94f" },
  critical: { label: "Critical", bg: "#fdecea", text: "#c0392b", ring: "#e05252" },
};

// ── sub-components ────────────────────────────────────────────────────────────
function StatusPill({ status }) {
  const meta = STATUS_META[status];
  if (!meta.label) return null;
  return (
    <span
      style={{
        fontSize: 11,
        fontWeight: 600,
        letterSpacing: "0.04em",
        padding: "2px 9px",
        borderRadius: 20,
        background: meta.bg,
        color: meta.text,
      }}
    >
      {meta.label.toUpperCase()}
    </span>
  );
}

function MetricCard({ metric, value, onChange }) {
  const status = getStatus(metric, value);
  const meta = STATUS_META[status];

  return (
    <div
      style={{
        background: "#fff",
        border: `1.5px solid ${status !== "empty" ? meta.ring : "#e8e8e8"}`,
        borderRadius: 14,
        padding: "16px 18px",
        display: "flex",
        flexDirection: "column",
        gap: 10,
        transition: "border-color 0.2s",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span
            style={{
              fontSize: 18,
              color: metric.color,
              lineHeight: 1,
              fontWeight: 700,
            }}
          >
            {metric.icon}
          </span>
          <span style={{ fontSize: 13, fontWeight: 600, color: "#222", letterSpacing: "0.01em" }}>
            {metric.label}
          </span>
        </div>
        <StatusPill status={status} />
      </div>

      <div style={{ position: "relative" }}>
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(metric.field, e.target.value)}
          placeholder={metric.placeholder}
          min={metric.min}
          max={metric.max}
          style={{
            width: "100%",
            boxSizing: "border-box",
            padding: "10px 48px 10px 14px",
            fontSize: 22,
            fontWeight: 700,
            color: status === "critical" ? meta.text : "#111",
            border: "none",
            background: "#f7f8fa",
            borderRadius: 10,
            outline: "none",
            fontFamily: "'DM Mono', monospace, sans-serif",
            appearance: "textfield",
            MozAppearance: "textfield",
            WebkitAppearance: "none",
          }}
        />
        <span
          style={{
            position: "absolute",
            right: 14,
            top: "50%",
            transform: "translateY(-50%)",
            fontSize: 12,
            fontWeight: 500,
            color: "#aaa",
            pointerEvents: "none",
          }}
        >
          {metric.unit}
        </span>
      </div>

      <div style={{ fontSize: 11, color: "#aaa" }}>
        Normal range: {metric.normalMin}–{metric.normalMax} {metric.unit}
      </div>
    </div>
  );
}

// ── main component ────────────────────────────────────────────────────────────
export default function HealthDailyUpdateForm({ userId, onSuccess }) {
  const [form, setForm] = useState({
    heart_rate: "",
    spo2: "",
    bp_systolic: "",
    bp_diastolic: "",
    timestamp: new Date().toISOString().slice(0, 16),
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
    setError(null);
  };

  const allStatuses = METRICS.map((m) => getStatus(m, form[m.field]));
  const hasCritical = allStatuses.includes("critical");
  const hasElevated = allStatuses.includes("elevated");
  const allEmpty = allStatuses.every((s) => s === "empty");

  const handleSubmit = async () => {
  setLoading(true);
  setError(null);

  const payload = {
    // user_id: userId ?? null,
    heart_rate: form.heart_rate !== "" ? parseInt(form.heart_rate, 10) : null,
    spo2: form.spo2 !== "" ? parseInt(form.spo2, 10) : null,
    bp_systolic: form.bp_systolic !== "" ? parseInt(form.bp_systolic, 10) : null,
    bp_diastolic: form.bp_diastolic !== "" ? parseInt(form.bp_diastolic, 10) : null,
    timestamp: form.timestamp
      ? new Date(form.timestamp).toISOString()
      : new Date().toISOString(),
  };
  console.log(payload)
  try {
    const result = await HealthDailyUpdate(payload);

    setSuccess(true);
    toast.success("Health Data Added")
    window.location.href="/home"
    onSuccess?.(result);
  } catch (err) {
    setError(err.message || "Failed to save. Please try again.");
  } finally {
    setLoading(false);
  }
};

  const handleReset = () => {
    setForm({
      heart_rate: "",
      spo2: "",
      bp_systolic: "",
      bp_diastolic: "",
      timestamp: new Date().toISOString().slice(0, 16),
    });
    setSuccess(false);
    setError(null);
  };

  // ── success state ─────────────────────────────────────────────────────────
  if (success) {
    return (
      <div style={styles.card}>
        <div style={{ textAlign: "center", padding: "2rem 1rem" }}>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: "50%",
              background: "#e8f7ef",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 26,
              margin: "0 auto 16px",
            }}
          >
            ✓
          </div>
          <h3 style={{ margin: "0 0 6px", fontSize: 18, fontWeight: 700, color: "#111" }}>
            Reading saved
          </h3>
          <p style={{ margin: "0 0 24px", fontSize: 14, color: "#888" }}>
            Your health data has been recorded successfully.
          </p>
          <button onClick={handleReset} style={styles.btnSecondary}>
            Add another reading
          </button>
        </div>
      </div>
    );
  }

  // ── form ──────────────────────────────────────────────────────────────────
  return (
    <div style={styles.card}>
      {/* header */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 24 }}>
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: 12,
            background: "#fdecea",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 20,
            color: "#e05252",
          }}
        >
          ♥
        </div>
        <div>
          <h2 style={{ margin: 0, fontSize: 17, fontWeight: 700, color: "#111" }}>
            Daily health update
          </h2>
          <p style={{ margin: 0, fontSize: 13, color: "#aaa" }}>
            {new Date().toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" })}
          </p>
        </div>
      </div>

      {/* alert banners */}
      {hasCritical && (
        <div style={{ ...styles.banner, background: "#fdecea", color: "#c0392b", borderColor: "#e05252" }}>
          ⚠ One or more values are outside the safe range
        </div>
      )}
      {!hasCritical && hasElevated && (
        <div style={{ ...styles.banner, background: "#fff8e8", color: "#b46800", borderColor: "#f7c94f" }}>
          ↑ Some values are above the normal range
        </div>
      )}

      {/* metrics grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: 12,
          marginBottom: 20,
        }}
      >
        {METRICS.map((m) => (
          <MetricCard key={m.field} metric={m} value={form[m.field]} onChange={handleChange} />
        ))}
      </div>

      {/* timestamp */}
      <div style={{ marginBottom: 20 }}>
        <label style={styles.label}>Reading timestamp</label>
        <input
          type="datetime-local"
          value={form.timestamp}
          onChange={(e) => handleChange("timestamp", e.target.value)}
          style={styles.input}
        />
      </div>

      {/* error */}
      {error && (
        <div style={{ ...styles.banner, background: "#fdecea", color: "#c0392b", borderColor: "#e05252", marginBottom: 12 }}>
          {error}
        </div>
      )}

      {/* actions */}
      <div style={{ display: "flex", gap: 10 }}>
        <button
          onClick={handleSubmit}
          disabled={loading || allEmpty}
          style={{
            ...styles.btnPrimary,
            opacity: loading || allEmpty ? 0.55 : 1,
            cursor: loading || allEmpty ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Saving…" : "Save reading"}
        </button>
        <button onClick={handleReset} style={styles.btnSecondary}>
          Clear
        </button>
      </div>
    </div>
  );
}

// ── styles ────────────────────────────────────────────────────────────────────
const styles = {
  card: {
    background: "#fff",
    borderRadius: 20,
    border: "1.5px solid #ebebeb",
    padding: "24px 24px 20px",
    maxWidth: 560,
    width: "100%",
    fontFamily: "'DM Sans', system-ui, sans-serif",
    boxSizing: "border-box",
  },
  label: {
    display: "block",
    fontSize: 13,
    fontWeight: 600,
    color: "#555",
    marginBottom: 6,
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "10px 14px",
    fontSize: 14,
    border: "1.5px solid #e8e8e8",
    borderRadius: 10,
    background: "#f7f8fa",
    color: "#111",
    outline: "none",
    fontFamily: "inherit",
  },
  banner: {
    fontSize: 13,
    fontWeight: 500,
    padding: "10px 14px",
    borderRadius: 10,
    border: "1px solid",
    marginBottom: 16,
  },
  btnPrimary: {
    flex: 1,
    padding: "12px 0",
    fontSize: 14,
    fontWeight: 700,
    color: "#fff",
    background: "#111",
    border: "none",
    borderRadius: 12,
    cursor: "pointer",
    letterSpacing: "0.02em",
    transition: "background 0.15s",
  },
  btnSecondary: {
    padding: "12px 20px",
    fontSize: 14,
    fontWeight: 600,
    color: "#555",
    background: "#f4f4f4",
    border: "none",
    borderRadius: 12,
    cursor: "pointer",
    transition: "background 0.15s",
  },
};
