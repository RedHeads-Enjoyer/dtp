import type {ForecastPoint} from "../../types.ts";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import {COLORS} from "./colors.ts";

type ForecastSectionProps = {
  data: ForecastPoint[]
}

export const ForecastSection = ({ data }: ForecastSectionProps) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} interval={Math.floor(data.length / 8)} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line dataKey="actual"   name={"Данные"}   stroke={COLORS.actual}   strokeWidth={2}    />
        <Line dataKey="baseline" name={"Базовая"}  stroke={COLORS.baseline} dot={{ r: 4 }} strokeWidth={2} />
        <Line dataKey="ridge"    name={"Ridge"}    stroke={COLORS.ridge}    dot={{ r: 4 }} strokeWidth={2} />
        <Line dataKey="lgbm"     name={"LightGBM"} stroke={COLORS.lgbm}     dot={{ r: 4 }} strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
};