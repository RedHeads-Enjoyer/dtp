import {Fragment} from "react";

import {Route, Routes} from "react-router-dom";
import {RawDtps} from "./view/RawDtps.tsx";
import {Uploader} from "./view/Uploader.tsx";
import {Header} from "./components/Header/Header.tsx";
import {WeatherRaw} from "./view/WeatherRaw.tsx";
import {WeatherParsed} from "./view/WeatherParsed.tsx";
import {Daily} from "./view/Daily.tsx";
import {Features} from "./view/Features.tsx";
import {Baseline} from "./view/Baseline.tsx";
import {WeatherClean} from "./view/WeatherClean.tsx";

export const App = () => {
    return (
        <Fragment>
            <Header />

            <Routes>
                <Route path="/upload" element={<Uploader />} />
                <Route path="/data_raw" element={<RawDtps />} />
                <Route path="/data_clean" element={<Daily />} />
                <Route path="/weather_raw" element={<WeatherRaw />} />
                <Route path="/weather_parsed" element={<WeatherParsed />} />
                <Route path="/weather_clean" element={<WeatherClean />} />
                <Route path="/features" element={<Features />} />
                <Route path="/baseline" element={<Baseline />} />
            </Routes>
        </Fragment>
    );
}