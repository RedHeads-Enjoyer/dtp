import type { MouseEventHandler, ReactNode } from "react";
import './styles.css'
import {Loader} from "../Loader/Loader.tsx";

type ButtonProps = {
  onClick: MouseEventHandler<HTMLButtonElement>;
  disabled?: boolean;
  loading?: boolean;
  children: ReactNode;
};

export const Button = ({ onClick, disabled = false, loading = false, children }: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled} className="button">
      {loading && <Loader size={15} label={null}/>}
      {children}
    </button>
  );
};