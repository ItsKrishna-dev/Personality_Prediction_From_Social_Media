import { useLocation, useNavigate } from "react-router-dom";
import { PersonalityResults } from "@/components/PersonalityResults";
import { useEffect } from "react";

interface TraitScore {
  score: number;
  percentage: number;
}

interface PredictionResponse {
  scores: Record<string, TraitScore>;
  interpretations: Record<string, string>;
  summary: {
    full_summary?: string;
    strengths?: string;
    growth_areas?: string;
    career_suggestions?: string;
  };
  success: boolean;
}

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results as PredictionResponse;

  useEffect(() => {
    // Redirect to analyze page if no results found
    if (!results) {
      navigate("/analyze");
    }
  }, [results, navigate]);

  if (!results) {
    return null;
  }

  const handleReset = () => {
    navigate("/analyze");
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full flex items-center justify-center">
        <PersonalityResults
          scores={results.scores}
          interpretations={results.interpretations}
          summary={results.summary}
          onReset={handleReset}
        />
      </div>
    </div>
  );
};

export default Results;
