import React, {useEffect, useState} from "react";

export default function () {
    const [isConnectedToApiSocket, setConnected] = useState(false);
    const [lastRequest, setLastRequest] = useState({
        image: "https://placehold.it/128x128"
    });
    const [lastResult, setLastResult] = useState({
        outcome: [{label: "A", chance: "90%"}, {label: "B", chance: "80%"}]
    });
    const [progress, setLastProgress] = useState({})

    const openSocket = () => {
        const ws = new WebSocket("wss://echo.websocket.org");
        ws.onclose = () => {
            setConnected(false);
            setTimeout(openSocket, 1000);
        };
        ws.onerror = e => {
            console.error(e);
            setConnected(false)
        };
        ws.onopen = () => {
            setConnected(true);
        };
        ws.onmessage = message => {
            const body = JSON.parse(message.data);
            switch (body.type) {
                case "request":
                    setLastRequest(body);
                    break;
                case "result":
                    setLastResult(body);
                    break;
                default:
                    break;
            }
        }
    };
    useEffect(openSocket, []);

    return (
        <>
            <div>
                <h1>Dashboard ML</h1>
                <p>{isConnectedToApiSocket ? "Connected" : "Connecting..."} to the server at port 5000</p>
                <img src={lastRequest.image} alt={""}/>
                <table>
                    <thead>
                        <tr>
                            <th>Label</th>
                            <th>Probability</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lastResult.outcome.map((it, index) => <tr key={index}>
                            <td>{it.label}</td>
                            <td>{it.chance}</td>
                        </tr>)}
                    </tbody>
                </table>
            </div>
        </>
    )
}