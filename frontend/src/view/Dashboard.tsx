import {useDashboard} from "../hooks/useDashboard.ts";
import type {Metric} from "../types.ts";
import {Loader} from "../components/Loader/Loader.tsx";
import {MetricBarChart} from "../components/Charts/MetricBarChart.tsx";
import {ForecastSection} from "../components/Charts/ForecastSection.tsx";
import {COLORS} from "../components/Charts/colors.ts";



export const Dashboard = () => {
  const { data, loading } = useDashboard();

  if (loading) return <Loader />;
  if (!data)   return <div>Нет данных. Сначала запустите модели.</div>;

  const nextDate = data.forecast.at(-1)?.date ?? "";
  const historyLen = data.forecast.length - 1;

  return (
    <div>
      <h3>Сравнение ошибок моделей (тест)</h3>
      <MetricsSection metrics={data.metrics}/>
      <h3>Последние {historyLen} дней и прогноз на {nextDate}</h3>
      <ForecastSection data={data.forecast} />
    </div>
  );
}

type MetricsSectionProps = {
  metrics: Metric[];
}

const MetricsSection = ({ metrics }: MetricsSectionProps) => {
  const maeData  = metrics.map((m) => ({ name: m.model_name, MAE:  m.mae_test  }));
  const maseData = metrics.map((m) => ({ name: m.model_name, MASE: m.mase_test, isBest: m.is_best }));

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
      <MetricBarChart title="MAE"  dataKey="MAE"  data={maeData}  color={COLORS.baseline} />
      <MetricBarChart title="MASE" dataKey="MASE" data={maseData} color={COLORS.ridge} />
    </div>
  );
};