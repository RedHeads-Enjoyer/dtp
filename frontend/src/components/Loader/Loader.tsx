import './styles.css'

type LoaderProps = {
  size?: number;
  label?: string | null;
};

export const Loader = ({ size = 20, label = "Загрузка..." }: LoaderProps) => {
  return (
    <span className="loader" role="status" aria-live="polite">
      <span
        className="loader-spinner"
        style={{ width: size, height: size }}
        aria-hidden="true"
      />
      {label && <span className="loader-label">{label}</span>}
    </span>
  );
};