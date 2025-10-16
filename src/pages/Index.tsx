import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Brain, Sparkles, TrendingUp, Users } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-primary-glow/20 rounded-full blur-3xl animate-pulse delay-1000" />
      </div>

      <div className="relative z-10 max-w-5xl mx-auto text-center space-y-8">
        {/* Hero Section */}
        <div className="space-y-6 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">AI-Powered Personality Analysis</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold leading-tight">
            Discover Your{" "}
            <span className="text-gradient">True Self</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto">
            Uncover your unique personality traits with advanced AI analysis based on the Big Five personality model
          </p>
        </div>

        {/* CTA Button */}
        <div className="animate-fade-in" style={{ animationDelay: "0.2s" }}>
          <Button 
            size="lg" 
            className="text-lg px-8 py-6 shadow-glow hover:scale-105 transition-all duration-300"
            onClick={() => navigate("/analyze")}
          >
            <Brain className="w-5 h-5 mr-2" />
            Get Started
          </Button>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-16 animate-fade-in" style={{ animationDelay: "0.4s" }}>
          <div className="bg-card/50 backdrop-blur-sm p-6 rounded-2xl border border-border shadow-card hover:shadow-glow transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 mx-auto">
              <Brain className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Scientific Accuracy</h3>
            <p className="text-sm text-muted-foreground">
              Based on the validated Big Five personality model used by psychologists worldwide
            </p>
          </div>

          <div className="bg-card/50 backdrop-blur-sm p-6 rounded-2xl border border-border shadow-card hover:shadow-glow transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 mx-auto">
              <Sparkles className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">AI-Powered Insights</h3>
            <p className="text-sm text-muted-foreground">
              Advanced AI generates personalized summaries and detailed trait interpretations
            </p>
          </div>

          <div className="bg-card/50 backdrop-blur-sm p-6 rounded-2xl border border-border shadow-card hover:shadow-glow transition-all duration-300 hover:scale-105">
            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 mx-auto">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Growth Opportunities</h3>
            <p className="text-sm text-muted-foreground">
              Discover your strengths and areas for personal development with actionable insights
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
