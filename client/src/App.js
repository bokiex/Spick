import logo from "./logo.svg";
import "./App.css";

function App() {
    const { data, setData } = useState([{}]);

    useEffect(() => {
        fetch("/members")
            .then((res) => res.json())
            .then((data) => setData(data));
    });
    return <div></div>;
}

export default App;
