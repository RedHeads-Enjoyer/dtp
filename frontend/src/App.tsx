import {Fragment} from "react";

import {Route, Routes} from "react-router-dom";
import {Data} from "./view/Data.tsx";
import {Dash} from "./view/Dash.tsx";
import {Uploader} from "./view/Uploader.tsx";
import {Header} from "./components/Header/Header.tsx";

export const App = () => {
    return (
        <Fragment>
            <Header />

            <Routes>
                <Route path="/upload" element={<Uploader />} />
                <Route path="/data" element={<Data />} />
                <Route path="/dash" element={<Dash />} />
            </Routes>
        </Fragment>
    );
}