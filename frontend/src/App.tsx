import { Navigate, Route, Routes } from "react-router-dom";

import { CreateModelingJobPage } from "./pages/CreateModelingJobPage";
import { ModelingResultPage } from "./pages/ModelingResultPage";

export default function App() {
  return (
    <main className="min-h-screen bg-black px-6 py-10 text-[#f0f0fa] font-din">
      <Routes>
        <Route path="/" element={<CreateModelingJobPage />} />
        <Route path="/jobs/:jobId" element={<ModelingResultPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </main>
  );
}
