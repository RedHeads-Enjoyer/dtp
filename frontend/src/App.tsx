import {Fragment} from "react";

import {Route, Routes} from "react-router-dom";
import {Dtps} from "./view/Dtps.tsx";
import {Uploader} from "./view/Uploader.tsx";
import {Header} from "./components/Header/Header.tsx";
import {RawWeather} from "./view/RawWeather.tsx";
import {Weather} from "./view/Weather.tsx";

export const App = () => {
    return (
        <Fragment>
            <Header />

            <Routes>
                <Route path="/upload" element={<Uploader />} />
                <Route path="/data" element={<Dtps />} />
                <Route path="/raw_weather" element={<RawWeather />} />
                <Route path="/weather" element={<Weather />} />
            </Routes>
        </Fragment>
    );
}