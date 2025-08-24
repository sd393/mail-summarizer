function ListGroup() {
    let items = [
        "London",
        "New York",
        "Paris",
        "Tokyo"
    ];

    //items = [];

    return (
        <>
            <h1>List</h1>

            {items.length === 0 && <p>No Items Found</p>};

            <ul className="list-group">
                {items.map((item) => (
                    <li key={item}>{item}</li>
                ))}
            </ul>
        </>
    );
}

export default ListGroup;