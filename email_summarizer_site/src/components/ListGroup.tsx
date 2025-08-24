import { useState } from "react";

function ListGroup() {
  let items = ["London", "New York", "Paris", "Tokyo"];
  let selectedIndex = 0;

  useState

  return (
    <>
      <h1>List</h1>

      {items.length === 0 && <p>No Items Found</p>}

      <ul className="list-group">
        {items.map((item, index) => (
          <li
            className={ selectedIndex === index ? "list-group-item active" : "list-group-item"}
            key={item}
            onClick={() => { selectedIndex = index;}}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
