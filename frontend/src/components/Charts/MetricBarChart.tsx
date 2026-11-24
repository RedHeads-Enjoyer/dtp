import './styles.css'
import {Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";

type MetricBar = {
  name: string;
  MAE?: number;
  MASE?: number;
  isBest?: boolean;
}

type MetricBarChartProps = {
  title:      string;
  dataKey:    string;
  data:       MetricBar[];
  color:      string;
}


export const MetricBarChart = ({ title, dataKey, data, color }: MetricBarChartProps) => {
  return (
    <div>
      <p className={"title"}>{title}</p>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar
          dataKey={dataKey}
          name={title}
          fill={color}
          shape={(props: any) => {
            const { x, y, width, height, index } = props;
            const isBest = data[index]?.isBest;
            return (
              <rect
                x={x}
                y={y}
                width={width}
                height={height}
                fill={isBest ? "#16a34a" : color}
                rx={4}
                ry={4}
              />
            );
          }}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
    );
};