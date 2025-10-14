import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { Brain, RotateCcw, Sparkles } from "lucide-react";

interface TraitScore {
  score: number;
  percentage: number;
}

interface PersonalityResultsProps {
  scores: Record<string, TraitScore>;
  interpretations: Record<string, string>;
  summary: {
    full_summary?: string;
    strengths?: string;
    growth_areas?: string;
    career_suggestions?: string;
  };
  onReset: () => void;
}

const TRAIT_COLORS = {
  Openness: "hsl(var(--openness))",
  Conscientiousness: "hsl(var(--conscientiousness))",
  Extraversion: "hsl(var(--extraversion))",
  Agreeableness: "hsl(var(--agreeableness))",
  Neuroticism: "hsl(var(--neuroticism))",
};

const TRAIT_DESCRIPTIONS = {
  Openness: "Imagination, creativity, and openness to new experiences",
  Conscientiousness: "Organization, dependability, and goal-oriented behavior",
  Extraversion: "Sociability, energy, and positive emotions",
  Agreeableness: "Compassion, cooperation, and trust in others",
  Neuroticism: "Emotional sensitivity and tendency toward negative emotions",
};

export const PersonalityResults = ({
  scores,
  interpretations,
  summary,
  onReset,
}: PersonalityResultsProps) => {
  const chartData = Object.entries(scores).map(([trait, data]) => ({
    name: trait,
    value: data.percentage,
    score: data.score,
  }));

  return (
    <div className="w-full max-w-6xl space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="flex items-center justify-center gap-2">
          <Brain className="h-8 w-8 text-primary" />
          <h1 className="text-4xl font-bold text-gradient">Your Personality Profile</h1>
        </div>
        <p className="text-muted-foreground text-lg">
          Based on the Big Five personality traits model
        </p>
      </div>

      {/* Chart and Traits Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <Card className="shadow-card border-border/50 backdrop-blur-sm bg-card/80">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              Trait Distribution
            </CardTitle>
            <CardDescription>Visual representation of your personality traits</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  animationBegin={0}
                  animationDuration={800}
                >
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={TRAIT_COLORS[entry.name as keyof typeof TRAIT_COLORS]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="bg-card border border-border rounded-lg p-3 shadow-lg">
                          <p className="font-semibold">{data.name}</p>
                          <p className="text-sm text-muted-foreground">
                            Score: {data.score}/10
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {data.value}%
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Trait Cards */}
        <div className="space-y-3">
          {Object.entries(scores).map(([trait, data]) => (
            <Card
              key={trait}
              className="shadow-card border-l-4 transition-all hover:shadow-glow"
              style={{
                borderLeftColor: TRAIT_COLORS[trait as keyof typeof TRAIT_COLORS],
              }}
            >
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-lg">{trait}</h3>
                    <p className="text-xs text-muted-foreground">
                      {TRAIT_DESCRIPTIONS[trait as keyof typeof TRAIT_DESCRIPTIONS]}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-primary">{data.score}/10</p>
                    <p className="text-xs text-muted-foreground">{data.percentage}%</p>
                  </div>
                </div>
                <p className="text-sm mt-2">{interpretations[trait]}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* AI Summary */}
      {summary && (
        <Card className="shadow-glow border-primary/20 backdrop-blur-sm bg-card/80">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              AI-Powered Personality Summary
            </CardTitle>
            <CardDescription>Generated insights about your personality</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {summary.full_summary && (
              <div>
                <h4 className="font-semibold mb-2 text-primary">Overview</h4>
                <p className="text-sm leading-relaxed whitespace-pre-line">
                  {summary.full_summary}
                </p>
              </div>
            )}
            
            {summary.strengths && (
              <div>
                <h4 className="font-semibold mb-2 text-primary">Your Strengths</h4>
                <p className="text-sm leading-relaxed whitespace-pre-line">
                  {summary.strengths}
                </p>
              </div>
            )}
            
            {summary.growth_areas && (
              <div>
                <h4 className="font-semibold mb-2 text-primary">Areas for Growth</h4>
                <p className="text-sm leading-relaxed whitespace-pre-line">
                  {summary.growth_areas}
                </p>
              </div>
            )}
            
            {summary.career_suggestions && (
              <div>
                <h4 className="font-semibold mb-2 text-primary">Career Suggestions</h4>
                <p className="text-sm leading-relaxed whitespace-pre-line">
                  {summary.career_suggestions}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Reset Button */}
      <div className="flex justify-center">
        <Button
          onClick={onReset}
          variant="outline"
          size="lg"
          className="shadow-card hover:shadow-glow transition-all"
        >
          <RotateCcw className="h-4 w-4 mr-2" />
          Take Test Again
        </Button>
      </div>
    </div>
  );
};
