import { useEffect, useState } from "react";
import {Loader} from "../Loader/Loader.tsx";
import "./styles.css";

type Props = {
  url: string;
  readyText?: string;
  staleText?: string;
  loaderLabel?: string;
};

type Status = "loading" | "ready" | "stale" | "error";

export const ReadyStatus = ({
  url,
  readyText = "актуальны",
  staleText = "не актуальны",
  loaderLabel = "Загрузка статуса",
}: Props) => {
  const [status, setStatus] = useState<Status>("loading");
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        const ready = (await res.json()) as boolean;
        setStatus(ready ? "ready" : "stale");
      } catch (e) {
        setMessage(
          e instanceof Error && e.message.startsWith("HTTP")
            ? "Ошибка при загрузке"
            : "Нет связи с сервером"
        );
        setStatus("error");
      }
    };

    load();
  }, [url]);

  const isReady = status === "ready";
  const isStale = status === "stale";

  return (
    <div className={"wrapper"}>
      {status === "loading" && <Loader label={loaderLabel} />}
      {status === "error" && <span className={"error"}>{message}</span>}
      {isReady && <span className={"ready"}>
          Данные {readyText}
        </span>
      }
      {isStale && <span className={"stale"}>
          Данные {staleText}
        </span>
      }
    </div>
  )
};