# Compound Pattern으로 정렬 가능한 Table 컴포넌트 만들기

## 1. 정렬 가능한 Table Component 만들기

특정 정보들을 Table 형태로 보여주고, 이 중 Header 부분을 클릭하면 클릭한 부분을 정렬하는 Sortable Table 컴포넌트를 만들고 싶다. 예상되는 모양은 다음과 같다.

<iframe height="300" style="width: 100%;" scrolling="no" title="Untitled" src="https://codepen.io/junhyeong-b/embed/wvErrYV?default-tab=html%2Cresult" frameborder="no" loading="lazy" allowtransparency="true" allowfullscreen="true">
  See the Pen <a href="https://codepen.io/junhyeong-b/pen/wvErrYV">
  Untitled</a> by Bae-Junhyeong (<a href="https://codepen.io/junhyeong-b">@junhyeong-b</a>)
  on <a href="https://codepen.io">CodePen</a>.
</iframe>

> **[Sortable Table Example](https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/)**

<br />

회사에서 `SortableTable.js` 라는 이름의 컴포넌트를 마이그레이션할 순간이 왔었다. 몇년 전부터 작성되어 유지보수 없이 사용되고 있었고, 해당 컴포넌트를 사용해 새로운 컴포넌트를 만드려면 Props를 새로 추가해야 했고, 바로바로 코드의 내용을 이해하기 어려웠다.

```jsx
// 대략적인 SortableTable 컴포넌트 사용 방법
import React from "react";

const MyComponent = ({ data }) => {
  const getColumns = () => [
    {
      id: "id1",
      className: "class1",
      label: "label1",
      orderBy: (row) => orderFunc(row),
      render: () => <div>render1</div>,
      sortable: true,
    },
    {
      id: "id2",
      className: "class2",
      label: "label2",
      orderBy: (row) => orderFunc(row),
      render: () => <div>render2</div>,
      sortable: true,
    },
    {
      id: "id3",
      className: "class3",
      label: "label3",
      orderBy: (row) => orderFunc(row),
      render: () => <div>render3</div>,
      sortable: true,
    },
  ];

  return <SortableTable columns={getColumns()} data={data} />;
};

export default MyComponent;
```

여기선 일부분의 예시만 들어서 간단해 보일 수 있지만, 실제로는 다른 컴포넌트와 결합하여 함께 사용되면서 읽기가 까다로웠다. 이렇게 사용할 경우 문제가 될만한 부분을 추려보면 다음과 같다.

- 코드 가독성이 좋지 않다.
- 각 Column 또는 Row 별로 스타일을 지정하기가 어렵다. SortableTable 자체적으로 스타일을 갖고 있어서 클래스 선택자를 중첩해서 사용해야 했다.
- 각 Column은 render 항목을 갖고 있어서 IDE 바로가기 등의 기능을 이용할 수 없고, 특정 부분을 수정하려면 찾기(`Ctrl + F` or `Command + F`)로 확인하거나 하나씩 살펴봐야 한다.
- SortableTable 자체적으로 정렬 기능을 제공하지만 orderBy 라는 항목을 따로 넘겨주고 있고, 무엇을 하는 코드인지 예측하기 어렵다.

<br />

해당 코드들을 마이그레이션하기 위해 살펴본 후 컴파운드 패턴으로 마이그레이션하면 좋을 것 같다는 생각이 들었고, 궁극적으로 SortableTable 컴포넌트 자체는 **정렬 기능만 제공**하고, 필요한 스타일은 사용하는 곳에서 지정하면 좀 더 유연하게 컴포넌트를 사용할 수 있을 것 같다고 생각했다.

<br />

## 2. Compound Pattern(컴파운드 패턴)

컴파운드 패턴은 여러 개의 하위 컴포넌트를 조합해서 하나의 컴포넌트를 만드는 패턴이다. 이 패턴을 이용하면 Props Drilling을 피할 수 있고, 기존의 컴포넌트를 재사용하면서 새로운 기능을 추가할 수 있어서 유지보수성이 높아진다.

SortableTable을 만들게 된다면, 이를 사용하는 쪽의 코드는 다음과 같은 구조를 가질 것이다.

```jsx
const TableDemo = ({ data }) => {
  return (
    <Table>
      <Table.Header>
        <Table.Column id="firstName">First Name</Table.Column>
        <Table.Column id="lastName">Last Name</Table.Column>
        <Table.Column id="email">Email</Table.Column>
        <Table.Column id="department">Department</Table.Column>
        <Table.Column id="jobTitle">Job Title</Table.Column>
      </Table.Header>

      <Table.Body>
        {data.map((item) => (
          <Table.Row key={item.id}>
            <Table.Cell>{item.firstName}</Table.Cell>
            <Table.Cell>{item.lastName}</Table.Cell>
            <Table.Cell>{item.email}</Table.Cell>
            <Table.Cell>{item.department}</Table.Cell>
            <Table.Cell>{item.jobTitle}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
```

- 모든 내용을 props로 내려주는 대신 data만 넘겨주고 필요에 따라 UI를 구성할 수 있다.
- `<Table.Cell />`, `<Table.Row />`등의 컴포넌트에 스타일을 지정할 수 있다.
- 기존 구조에 비해 상대적으로 구조를 파악하기 쉽다.

그럼 위와 같은 구조를 어떻게 만들 수 있을지 알아보자.

<br />

## 3. 각 UI를 구성하는 Table 컴포넌트 만들기

### 3-1) Body

```tsx
// TableBody
import React from "react";

interface Props {
  className?: string;
}

const TableBody = ({ className, children }: React.PropsWithChildren<Props>) => {
  return <tbody className={className}>{children}</tbody>;
};

const TableRow = ({ children, className }: React.PropsWithChildren<Props>) => {
  return <tr className={className}>{children}</tr>;
};

const TableCell = ({ children, className }: React.PropsWithChildren<Props>) => {
  return <td className={className}>{children}</td>;
};
```

Body에 해당하는 부분은 사실상 데이터를 사용자에게 보여주기만 하면 돼서 복잡한 구현이 필요하진 않다. 필요에 따라 다른 Props를 추가하면 된다.

<br />

### 3-2) Header

**TableHeader.tsx**

```tsx
// TableHeader.tsx
import React from "react";
import { SortingDirection } from "../types";

interface Props<T> {
  children: React.ReactNode;
  className?: string;
  isSortableHeader: boolean;
  onSort: (sortKey: keyof T, sortDir?: SortingDirection) => void;
  rowClassName?: string;
  sortDir: SortingDirection;
  sortKey: keyof T;
}

const TableHeader = <T,>({
  children,
  className,
  isSortableHeader,
  onSort,
  rowClassName,
  sortDir,
  sortKey,
}: Props<T>) => {
  const headerChildrens = isSortableHeader
    ? React.Children.map(children, (child) =>
        React.cloneElement(child as React.ReactElement<Props<T>>, {
          onSort,
          isSortableHeader,
          sortKey,
          sortDir,
        })
      )
    : children;
  return (
    <thead className={className}>
      <tr className={rowClassName}>{headerChildrens}</tr>
    </thead>
  );
};

export default TableHeader;
```

- **onSort**: 어떤 항목에 대해 정렬할 지 key 값을 인자로 받는 정렬 함수
- **sortDir**: 오름차순, 내림차순, 정렬안함 3가지 상태를 갖는 (`"asc" | "desc" | "none"`)
- **sortKey**: 어떤 항목에 대한 정렬인지를 알려주는 key값 (`string`)
- **isSortableHeader**: 정렬 가능한 테이블인지 아닌지에 대한 값 (`boolean`) 해당 값이 true인 경우만 정렬 가능.
- **Generic <T>**: 어떤 Data가 들어올지 모르므로 제네릭 타입을 사용하고, 사용하는 쪽에서 타입 추론이 가능하도록 `cloneElement` 메서드에서의 매개변수 child에 Props<T> 값을 넘겨준다.

위와 같은 Props를 받고, Header 내부에 `<th />` 태그로 이루어진 항목들을 children으로 받을 예정이므로 모든 props들을 children으로 내려준다. 이렇게 하면 `<th />` 각각에 onSort 등과 같은 props를 매번 써주지 않아도 되고, 하나의 onSort, sortKey 등을 공유하게 되므로 불필요한 코드를 줄일 수 있다.

<br />

**TableColumn.tsx**

```tsx
// TableColumn
import React from "react";
import { SortingDirection } from "../types";

interface Props<T> {
  children: React.ReactElement | string;
  className?: string;
  id?: keyof T;
  isSortableHeader?: boolean;
  onSort?: (sortKey: keyof T) => T[];
  sortDir?: SortingDirection;
  sortKey?: keyof T;
}

const TableColumn = <T,>({
  children,
  className,
  id,
  isSortableHeader,
  onSort,
  sortDir,
  sortKey,
}: Props<T>) => {
  const isArrowVisible =
    isSortableHeader && sortKey === id && sortDir !== "none";

  const onColumnHeaderClick = () => {
    id && onSort?.(id);
  };

  return (
    <th
      onClick={onColumnHeaderClick}
      className={cx(className, {
        [rootCss]: isSortableHeader,
      })}
    >
      {children}
    </th>
  );
};

export default TableColumn;
```

- isSortableHeader 값에 따라 정렬 기능이 없는 Table로 사용할 수도 있으므로 위에서 설명한 Props들은 전부 Optional한 값으로 타입을 지정한다.
- id 값을 통해 현재 정렬하려는 Column인지 아닌지 판별.
- id, onSort 등은 모두 정렬이 가능한 Table일 때만 필요하므로 방어코드 작성.

<br />

### 3-3) Sorting 기능을 하는 Hook 구현

**useSort.ts**

```tsx
import orderBy from "@/utils/orderBy";
import { useMemo, useRef, useState } from "react";
import { SortingDirection } from "./types";

interface Sorter<T> {
  sortKey: keyof T;
  sortDir: SortingDirection;
}

interface UseSortProps<T> {
  data: T[];
  customSorterFunc?: ({
    items,
    sortKey,
    sortDir,
  }: {
    items: T[];
    sortKey: keyof T;
    sortDir: SortingDirection;
  }) => T[];
}

const useSort = <T,>({
  sortKey = "" as keyof T,
  sortDir = "none",
  data,
  customSorterFunc = sortBySorting,
}: Partial<Sorter<T>> & UseSortProps<T>) => {
  const defaultSorter = useRef(customSorterFunc);
  const [sorter, setSorter] = useState<Sorter<T>>({
    sortKey,
    sortDir,
  });

  const onSort = (nextSortKey: keyof T, nextSortDir?: SortingDirection) => {
    const nextDirection =
      nextSortDir ??
      (sorter.sortKey !== nextSortKey
        ? "asc"
        : getNextSortDirection(sorter.sortDir));

    setSorter({
      sortKey: nextSortKey,
      sortDir: nextDirection,
    });
  };

  const sortedItems = useMemo(
    () =>
      defaultSorter.current({
        items: data,
        sortKey: sorter.sortKey,
        sortDir: sorter.sortDir,
      }),
    [data, sorter]
  );

  return { onSort, sortedItems, ...sorter };
};

export default useSort;

const getNextSortDirection = (
  currentDirection: SortingDirection
): SortingDirection => {
  switch (currentDirection) {
    case "asc":
      return "desc";
    case "desc":
      return "none";
    case "none":
    default:
      return "asc";
  }
};

const sortBySorting = <T,>({
  items,
  sortKey,
  sortDir,
}: {
  items: T[];
  sortKey: keyof T;
  sortDir: SortingDirection;
}): T[] => {
  switch (sortDir) {
    case "asc":
    case "desc":
      return orderBy(items, (item: T) => item[sortKey], sortDir);
    case "none":
    default:
      return items;
  }
};
```

- **useSort**: 정렬 기능을 하는 **onSort**, 정렬이 완료된 **sortedItems**, 정렬 방향 및 정렬하려는 행을 나타내는 **sortKey**, **sortDir** 값을 반환하는 Hook.
- **getNextSortDirection**: 정렬 방향을 전환시켜주는 함수. 정렬 안함 → 오름차순 → 내림차순 → 정렬 안함 순환.
- **sortBySorting**: 각 정렬 방식에 따라 정렬된 데이터를 반환.

<br />

### 3-4) 모든 내용을 포괄하는 Table 컴포넌트

**Table.tsx**

```tsx
import React from "react";
import TableBody from "./Body/TableBody";
import TableCell from "./Body/TableCell";
import TableRow from "./Body/TableRow";
import TableColumn from "./Header/TableColumn";
import TableHeader from "./Header/TableHeader";

interface Props {
  children: React.ReactNode;
  className?: string;
}

const Table = ({ children, className }: Props) => {
  return <table className={className}>{children}</table>;
};

export default Table;

Table.Header = TableHeader;
Table.Column = TableColumn;
Table.Body = TableBody;
Table.Cell = TableCell;
Table.Row = TableRow;
```

<br />

## 4. 최종 컴포넌트의 사용 모습

```tsx
import React from "react";
import Table from "./Table";
import useSort from "./useSort";

interface Props {
  data: {
    id: number;
    firstName: string;
    lastName: string;
    email: string;
    department: string;
    jobTitle: string;
  }[];
}

const TableDemo = ({ data }: Props) => {
  const { onSort, sortedItems, sortDir, sortKey } = useSort({ data });
  return (
    <Table>
      <Table.Header
        onSort={onSort}
        sortDir={sortDir}
        sortKey={sortKey}
        isSortableHeader
      >
        <Table.Column id="firstName">First Name</Table.Column>
        <Table.Column id="lastName">Last Name</Table.Column>
        <Table.Column id="email">Email</Table.Column>
        <Table.Column id="department">Department</Table.Column>
        <Table.Column id="jobTitle">Job Title</Table.Column>
      </Table.Header>

      <Table.Body>
        {sortedItems.map((item) => (
          <Table.Row key={item.id}>
            <Table.Cell>{item.firstName}</Table.Cell>
            <Table.Cell>{item.lastName}</Table.Cell>
            <Table.Cell>{item.email}</Table.Cell>
            <Table.Cell>{item.department}</Table.Cell>
            <Table.Cell>{item.jobTitle}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};

export default TableDemo;
```

- `Table.Header` 컴포넌트는 `sortKey: keyof T` 항목을 통해 T 타입 추론이 가능하므로 제네릭 T 타입을 따로 지정해주지 않아도 된다.
- `Table.Header`에서 **onSort**, **sortKey**, **sortDir** 등의 값을 `children`으로 넘겨주므로 `Table.Column`에 해당 Props들을 지정하지 않아도 된다.
- `Table.Body`부분은 데이터를 보여주기만 하면 된다. 인터랙션이 필요하다면 Props를 추가하고 적절한 위치에 추가하면 된다.

<br />

<div align="center">
  <img src="https://user-images.githubusercontent.com/85148549/223630031-a5bb6ca5-80d3-4f37-8048-b43689358d5a.gif" />
</div>

## 5. 정리

`SortableTable.js`를 마이그레이션할 때 시간이 오래 걸렸다. 사용되는 모든 곳을 하나씩 확인해야 했고, 하드코딩 형태로 수정해야 했다. SortableTable 자체에 스타일을 갖고 있고, 사용되는 곳들의 디자인이 모두 달랐기 때문에 여기서 A 스타일을 주고 저기서 B 스타일을 주고 있어서 새로 만들어진 컴포넌트에서는 `A, B, C {}` 형태로 클래스 선택자 중첩을 사용하고 있었다. 이런 중첩을 제거하고 css-in-js 형태로 바꾸고 싶었지만 SortableTable을 사용하는 모든 컴포넌트가 마이그레이션이 완료 되어야 스타일을 걷어낼 수 있었고, 코드가 서로 엉켜 있어서 분명 A 컴포넌트에 수정을 했는데, B, C 에서도 디자인이 달라지는 현상도 있었다.

이걸 컴파운드 패턴으로 수정한다면 좀 더 유연하게 UI를 구성할 수 있게 되고, 정렬 기능만 제공하면 되므로 스타일 때문에 골치아플 일이 없을 것 같다고 생각했다. 기능은 Hook으로 분리하고, 각 컴포넌트에서는 어떤 식으로 사용할지에 따라 props를 구성하면 돼서 코드를 한 눈에 보기 쉬워진 것 같다.

---

## 참조

- [https://javascript.plainenglish.io/5-advanced-react-patterns-a6b7624267a6](https://javascript.plainenglish.io/5-advanced-react-patterns-a6b7624267a6)
- [https://dev.to/droopytersen/new-react-component-pattern-compound-components-w-a-hook-jgf](https://dev.to/droopytersen/new-react-component-pattern-compound-components-w-a-hook-jgf)
