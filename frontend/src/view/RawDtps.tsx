import { formatDate } from "../utils.ts";
import { List, type Column } from "../components/List/List.tsx";
import { useList } from "../hooks/useList.ts";
import type { DtpItem } from "../types.ts";

const columns: Column<DtpItem>[] = [
  { key: "date", header: "Дата", render: (i) => formatDate(i.datetime) },
  { key: "region", header: "Регион", render: (i) => i.region },
  {
    key: "address",
    header: "Адрес",
    render: (i) => i.address,
    className: "ellipsis",
  },
  { key: "category", header: "Категория", render: (i) => i.category },
  { key: "severity", header: "Тяжесть", render: (i) => i.severity },
  { key: "weather", header: "Погода", render: (i) => i.weather },
  { key: "participants", header: "Участников", align: "right", render: (i) => i.participants_count },
  { key: "dead", header: "Погибло", align: "right", render: (i) => i.dead_count },
  { key: "injured", header: "Ранено", align: "right", render: (i) => i.injured_count },
];

export const RawDtps = () => {
  const dtp = useList<DtpItem>({ url: "/api/raw_dtp" });

  return (
    <List
      items={dtp.items}
      total={dtp.total}
      columns={columns}
      loading={dtp.loading}
      emptyText="Нет данных"
      pager={{
        page: dtp.page,
        pages: dtp.pages ?? 0,
        onChange: dtp.setPage,
      }}
      getKey={(i) => i.id}
    />
  );
};