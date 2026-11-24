import './styles.css'

type ParamsProps = {
  params: Record<string, unknown>;
};

export const Params = ({ params }: ParamsProps) => {
  return (
    <div>
      {Object.entries(params).map(([key, value]) => (
          <div className={"params_wrapper"} key={key}>
            <div><b>{key}</b></div>
            <div>{String(value)}</div>
          </div>
        ))}
    </div>
  );
};