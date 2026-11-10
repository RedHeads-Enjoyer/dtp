import {Fragment} from "react";

import {Route, Routes} from "react-router-dom";
import {RawDtps} from "./view/RawDtps.tsx";
import {Uploader} from "./view/Uploader.tsx";
import {Header} from "./components/Header/Header.tsx";
import {RawWeather} from "./view/RawWeather.tsx";
import {Weather} from "./view/Weather.tsx";
import {Daily} from "./view/Daily.tsx";
import {Features} from "./view/Features.tsx";
import {Baseline} from "./view/Baseline.tsx";

export const App = () => {
    return (
        <Fragment>
            <Header />

            <Routes>
                <Route path="/upload" element={<Uploader />} />
                <Route path="/raw_data" element={<RawDtps />} />
                <Route path="/clean_data" element={<Daily />} />
                <Route path="/raw_weather" element={<RawWeather />} />
                <Route path="/weather" element={<Weather />} />
                <Route path="/features" element={<Features />} />
                <Route path="/baseline" element={<Baseline />} />
            </Routes>
        </Fragment>
    );
}