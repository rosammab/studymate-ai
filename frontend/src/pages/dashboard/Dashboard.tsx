
import {
  BookOpen,
  Layers,
  Brain,
  Clock,
  Flame,
  TrendingUp,
} from "lucide-react";

import { useQuery } from "@tanstack/react-query";

import {
  getProgressSummary,
  getRecentActivities,
  getDailyProgress,
} from "../../services/progressService";

export default function Dashboard() {
  const {
    data: progress,
    isLoading: progressLoading,
    error: progressError,
  } = useQuery({
    queryKey: ["progress-summary"],
    queryFn: getProgressSummary,
  });

  const {
    data: activities = [],
    isLoading: activitiesLoading,
    error: activitiesError,
  } = useQuery({
    queryKey: ["recent-activities"],
    queryFn: getRecentActivities,
  });

  const {
    data: dailyProgress,
    isLoading: dailyLoading,
  } = useQuery({
    queryKey: ["daily-progress"],
    queryFn: () => getDailyProgress(7),
  });

  const totalStudyHours = progress
    ? (progress.total_study_minutes / 60).toFixed(1)
    : "0.0";

  const weeklyMinutes =
    dailyProgress?.activities.reduce(
      (total, activity) => total + activity.total_minutes,
      0
    ) ?? 0;

  // Temporary weekly target: 20 hours.
  // Later we can connect this to the student's actual study goal.
  const weeklyTargetMinutes = 20 * 60;

  const weeklyPercentage = Math.min(
    Math.round((weeklyMinutes / weeklyTargetMinutes) * 100),
    100
  );

  const stats = [
    {
      title: "Study Hours",
      value: totalStudyHours,
      description: "Total learning time",
      icon: Clock,
    },
    {
      title: "Quizzes Completed",
      value: progress?.total_quizzes ?? 0,
      description: "Total quizzes recorded",
      icon: Brain,
    },
    {
      title: "Flashcards Reviewed",
      value: progress?.total_flashcards_reviewed ?? 0,
      description: "Total cards reviewed",
      icon: Layers,
    },
    {
      title: "Current Streak",
      value: `${progress?.current_streak ?? 0} days`,
      description: "Consecutive study days",
      icon: Flame,
    },
  ];

  if (progressLoading) {
    return <div className="dashboard-page">Loading dashboard data...</div>;
  }

  if (progressError) {
    return (
      <div className="dashboard-page">
        <h2>Unable to load dashboard</h2>
        <p>Please check your login and Django server connection.</p>
      </div>
    );
  }

  const recentActivities = [...activities]
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() -
        new Date(a.created_at).getTime()
    )
    .slice(0, 5);

  return (
    <div className="dashboard-page">
      <div className="welcome-section">
        <div>
          <p className="eyebrow">LEARNING OVERVIEW</p>
          <h1>Welcome back!</h1>
          <p className="welcome-text">
            Continue your learning journey. Every small step counts.
          </p>
        </div>
      </div>

      <div className="stats-grid">
        {stats.map((stat) => {
          const Icon = stat.icon;

          return (
            <div className="stat-card" key={stat.title}>
              <div className="stat-top">
                <div className="stat-icon">
                  <Icon size={22} />
                </div>
              </div>

              <h2>{stat.value}</h2>
              <h3>{stat.title}</h3>
              <p>{stat.description}</p>
            </div>
          );
        })}
      </div>

      <div className="dashboard-grid">
        <section className="content-card">
          <div className="section-heading">
            <div>
              <h2>Learning Progress</h2>
              <p>Your study activity over the last 7 days</p>
            </div>
            <TrendingUp size={22} />
          </div>

          {dailyLoading ? (
            <p>Loading weekly progress...</p>
          ) : (
            <div className="progress-content">
              <div
                className="progress-circle"
                style={{
                  background: `conic-gradient(#7664e8 ${weeklyPercentage}%, #eeecf8 ${weeklyPercentage}% 100%)`,
                }}
              >
                <div>
                  <strong>{weeklyPercentage}%</strong>
                  <span>Weekly goal</span>
                </div>
              </div>

              <div className="progress-details">
                <h3>Keep going!</h3>
                <p>
                  You studied {(weeklyMinutes / 60).toFixed(1)} hours
                  during the last 7 days.
                </p>

                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${weeklyPercentage}%` }}
                  />
                </div>

                <span>
                  {(weeklyMinutes / 60).toFixed(1)} / 20 hours
                </span>
              </div>
            </div>
          )}
        </section>

        <section className="content-card">
          <div className="section-heading">
            <div>
              <h2>Study Statistics</h2>
              <p>Your learning consistency</p>
            </div>
            <Flame size={22} />
          </div>

          <div className="goal-item">
            <div>
              <strong>Current streak</strong>
              <p>Consecutive days studied</p>
            </div>
            <span className="goal-number">
              {progress?.current_streak ?? 0} days
            </span>
          </div>

          <div className="goal-item">
            <div>
              <strong>Longest streak</strong>
              <p>Your personal record</p>
            </div>
            <span className="goal-number">
              {progress?.longest_streak ?? 0} days
            </span>
          </div>

          <div className="goal-item">
            <div>
              <strong>Total study time</strong>
              <p>All recorded study sessions</p>
            </div>
            <span className="goal-number">
              {totalStudyHours} hrs
            </span>
          </div>
        </section>
      </div>

      <section className="content-card activity-card">
        <div className="section-heading">
          <div>
            <h2>Recent Activities</h2>
            <p>Your latest learning activities</p>
          </div>
          <BookOpen size={22} />
        </div>

        {activitiesLoading ? (
          <p>Loading activities...</p>
        ) : activitiesError ? (
          <p>Unable to load activities.</p>
        ) : recentActivities.length === 0 ? (
          <p>No study activities recorded yet. Start learning!</p>
        ) : (
          recentActivities.map((activity) => (
            <div className="activity-item" key={activity.id}>
              <div className="activity-icon">
                <BookOpen size={20} />
              </div>

              <div className="activity-info">
                <strong>
                  {activity.activity_type.replace("_", " ")}
                </strong>
                <span>
                  {activity.count} activity record(s)
                  {" · "}
                  {activity.duration_minutes} minutes
                </span>
              </div>

              <span className="activity-time">
                {activity.activity_date}
              </span>
            </div>
          ))
        )}
      </section>
    </div>
  );
}
