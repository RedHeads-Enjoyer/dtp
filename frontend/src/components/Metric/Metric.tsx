import './styles.css'

type MetricsProps = {
  value: number;
};

export const Metric = ({ value }: MetricsProps) => {
  return (
    <div className={"metric_wrapper"}>
      {value.toFixed(5)}
    </div>
  );
};