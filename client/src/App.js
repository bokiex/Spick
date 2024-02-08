import "./App.css";
import React, { useState, useEffect } from "react";
function App() {
    const [data, setData] = useState([{}]);

    // simple fetch request to the server
    useEffect(() => {
        fetch("/members")
            .then((res) => res.json())
            .then((data) => {
                setData(data);
                console.log(data);
            });
    }, []);
    return (
        <div>
            {typeof data.members === "undefined" ? (
                <h1>Loading...</h1>
            ) : (
                data.members.map((member, index) => {
                    return (
                        <div key={index}>
                            <h1>{member}</h1>
                        </div>
                    );
                })
            )}
        </div>
    );
}

export default App;
