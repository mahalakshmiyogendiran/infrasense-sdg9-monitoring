import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function SensorChart({ readings }) {
  const chartData = readings.map((reading) => ({
    time: new Date(
      reading.timestamp
    ).toLocaleTimeString(),

    vibration: reading.vibration,
    strain: reading.strain,
    tilt: reading.tilt,
  }));

  if (chartData.length === 0) {
    return <p>No sensor readings available.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />

        <Line
          type="monotone"
          dataKey="vibration"
          stroke="#dc2626"
          name="Vibration"
        />

        <Line
          type="monotone"
          dataKey="strain"
          stroke="#2563eb"
          name="Strain"
        />

        <Line
          type="monotone"
          dataKey="tilt"
          stroke="#ca8a04"
          name="Tilt"
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default SensorChart;