import React, { useEffect, useState } from "react";

import {


  Sparkles,

  Clock,

  Target,

  Briefcase,

  BookOpen,

  Lightbulb,

  MessageSquare,

} from "lucide-react";



import {

  analyzeCareer,

  getRoles,

} from "../services/api";



function Dashboard() {

  const [targetJob, setTargetJob] = useState("");

  const [skills, setSkills] = useState("");

  const [studyTime, setStudyTime] = useState(10);

  const [experienceLevel, setExperienceLevel] = useState("Beginner");

  const [learningStyle, setLearningStyle] =

    useState("Project-Based");



  const [availableRoles, setAvailableRoles] = useState([]);

  const fallbackRoles = [
    "AI Engineer", "AI Developer", "Machine Learning Engineer",
    "Data Scientist", "Data Analyst", "Data Engineer",
    "ML Researcher", "NLP Engineer", "Computer Vision Engineer",
    "Generative AI Engineer", "Software Developer", "Software Engineer",
    "Full Stack Developer", "Frontend Developer", "Backend Developer",
    "Web Developer", "Python Developer", "Java Developer",
    "JavaScript Developer", "Mobile App Developer", "Cloud Engineer",
    "Cloud Architect", "DevOps Engineer", "Site Reliability Engineer",
    "Solutions Architect", "System Administrator", "Network Engineer",
    "Cybersecurity Engineer", "Cybersecurity Analyst", "Security Engineer",
    "Information Security Analyst", "Application Security Engineer",
    "Database Administrator", "Database Developer", "SQL Developer",
    "Database Engineer", "Business Analyst", "Product Manager",
    "QA Engineer", "Automation Test Engineer", "Technical Support Engineer",
    "IT Support Specialist", "UI/UX Designer"
  ];

  const [showSuggestions, setShowSuggestions] = useState(false);



  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");



  // Load ALL job roles from the dataset

  useEffect(() => {

    async function loadRoles() {

      try {

        const response = await getRoles();



        setAvailableRoles(

          response.roles || []

        );

      } catch (error) {

        console.error("Unable to load job roles:", error);
        setAvailableRoles(fallbackRoles);

      }

    }



    loadRoles();

  }, []);



  // Filter roles while typing

  const query = targetJob.trim().toLowerCase();

  const filteredRoles =
    query.length > 0
      ? [...availableRoles]
          .filter((role) => role.toLowerCase().includes(query))
          .sort((a, b) => {
            const aStarts = a.toLowerCase().startsWith(query);
            const bStarts = b.toLowerCase().startsWith(query);
            return Number(bStarts) - Number(aStarts);
          })
          .slice(0, 8)
      : [];



  const handleAnalyze = async () => {

    if (!targetJob.trim()) {

      setError("Please enter a target job role.");

      return;

    }



    if (!skills.trim()) {

      setError("Please enter your current skills.");

      return;

    }



    setLoading(true);

    setError("");

    setResult(null);



    try {

      const response = await analyzeCareer({

        target_job: targetJob.trim(),



        current_skills: skills

          .split(",")

          .map((skill) => skill.trim())

          .filter(Boolean),



        study_time: Number(studyTime),



        experience_level:

          experienceLevel,



        learning_style:

          learningStyle,

      });



      setResult(response.data);

    } catch (error) {

      console.error(error);



      setError(

        error.response?.data?.detail ||

          "Unable to analyze career."

      );

    } finally {

      setLoading(false);

    }

  };



  return (

    <div className="dashboard-page">



      {/* HERO */}

      <section className="hero-section">

        <div>

          <p className="eyebrow">

            AI CAREER NAVIGATOR

          </p>



          <h1>

            Build Your Career

            <br />

            <span>With AI Guidance</span>

          </h1>



          <p className="hero-description">

            Discover your skill gaps, create a

            personalized roadmap, and prepare

            for your target career.

          </p>

        </div>



        <div className="hero-icon">

          <Sparkles size={48} />

        </div>

      </section>



      {/* PROFILE INPUT */}

      <section className="profile-panel">



        <div className="section-heading">

          <Target size={22} />



          <div>

            <h2>

              Career Profile

            </h2>



            <p>

              Tell us about your career goal

              and current skills.

            </p>

          </div>

        </div>



        <div className="profile-grid">



          {/* TARGET JOB */}

          <div className="input-group">



            <label>

              Target Job Role

            </label>



            <div className="role-search">
<input

                type="text"

                value={targetJob}

                onChange={(event) => {

                  setTargetJob(

                    event.target.value

                  );



                  setShowSuggestions(true);

                  setError("");

                }}

                onFocus={() =>

                  setShowSuggestions(true)

                }

                placeholder="Type your target job..."

              />



              {showSuggestions &&

                filteredRoles.length > 0 && (



                  <div className="role-suggestions">



                    {filteredRoles.map(

                      (role) => (



                        <button

                          type="button"

                          key={role}

                          className="role-suggestion"

                          onClick={() => {

                            setTargetJob(role);

                            setShowSuggestions(false);

                          }}

                        >

                          <Briefcase

                            size={16}

                          />



                          <span>

                            {role}

                          </span>

                        </button>



                      )

                    )}



                  </div>

                )}



            </div>
</div>



          {/* CURRENT SKILLS */}

          <div className="input-group">



            <label>

              Current Skills

            </label>



            <input

              type="text"

              value={skills}

              onChange={(event) =>

                setSkills(event.target.value)

              }

              placeholder="Python, SQL, Java..."

            />



            <small>

              Separate skills with commas

            </small>



          </div>



          {/* STUDY TIME */}

          <div className="input-group">



            <label>

              Study Time

            </label>



            <div className="input-with-icon">



              <Clock size={18} />



              <input

                type="number"

                min="1"

                max="60"

                value={studyTime}

                onChange={(event) =>

                  setStudyTime(

                    event.target.value

                  )

                }

              />



              <span>

                hours/week

              </span>



            </div>



          </div>



          {/* EXPERIENCE */}

          <div className="input-group">



            <label>

              Experience Level

            </label>



            <select

              value={experienceLevel}

              onChange={(event) =>

                setExperienceLevel(

                  event.target.value

                )

              }

            >

              <option>

                Beginner

              </option>



              <option>

                Intermediate

              </option>



              <option>

                Advanced

              </option>

            </select>



          </div>



          {/* LEARNING STYLE */}

          <div className="input-group">



            <label>

              Learning Style

            </label>



            <select

              value={learningStyle}

              onChange={(event) =>

                setLearningStyle(

                  event.target.value

                )

              }

            >

              <option>

                Project-Based

              </option>



              <option>

                Practice-Based

              </option>



              <option>

                Theory-Based

              </option>

            </select>



          </div>



        </div>



        {error && (

          <div className="error-message">

            {error}

          </div>

        )}



        <button

          className="analyze-button"

          onClick={handleAnalyze}

          disabled={loading}

        >

          {loading

            ? "Analyzing..."

            : "Analyze My Career"}



          {!loading && (

            <Sparkles size={18} />

          )}

        </button>



      </section>



      {/* RESULTS */}

      {result && (

        <>

          {/* STATS */}

          <section className="stats-grid">



            <div className="stat-card">

              <div className="stat-icon">

                <Target />

              </div>



              <div>

                <span>

                  Readiness

                </span>



                <strong>

                  {result.readiness}%

                </strong>

              </div>

            </div>



            <div className="stat-card">

              <div className="stat-icon">

                <Briefcase />

              </div>



              <div>

                <span>

                  Target Role

                </span>



                <strong>

                  {result.target_job}

                </strong>

              </div>

            </div>



            <div className="stat-card">

              <div className="stat-icon">

                <BookOpen />

              </div>



              <div>

                <span>

                  Required Skills

                </span>



                <strong>

                  {result.required_skills?.length ||

                    0}

                </strong>

              </div>

            </div>



            <div className="stat-card">

              <div className="stat-icon">

                <Lightbulb />

              </div>



              <div>

                <span>

                  Missing Skills

                </span>



                <strong>

                  {result.missing_skills?.length ||

                    0}

                </strong>

              </div>

            </div>



          </section>



          {/* SKILL OVERVIEW */}

          <section className="dashboard-card">



            <div className="card-heading">



              <div>

                <h2>

                  Skill Overview

                </h2>



                <p>

                  Your current skills compared

                  with the target role.

                </p>

              </div>



            </div>



            <div className="skill-columns">



              <div>

                <h3>

                  Matching Skills

                </h3>



                {result.matching_skills?.length >

                0 ? (



                  <div className="skill-list">



                    {result.matching_skills.map(

                      (skill) => (



                        <div

                          className="skill-item matched"

                          key={skill}

                        >

                          ✓ {skill}

                        </div>



                      )

                    )}



                  </div>



                ) : (

                  <p>

                    No exact matching skills yet.

                  </p>

                )}



              </div>



              <div>

                <h3>

                  Missing Skills

                </h3>



                {result.missing_skills?.length >

                0 ? (



                  <div className="skill-list">



                    {result.missing_skills.map(

                      (skill) => (



                        <div

                          className="skill-item missing"

                          key={skill}

                        >

                          • {skill}

                        </div>



                      )

                    )}



                  </div>



                ) : (

                  <p>

                    No major skill gaps found.

                  </p>

                )}



              </div>



            </div>



          </section>



          {/* PRIORITY SKILLS */}

          <section className="dashboard-card">



            <div className="card-heading">



              <div>

                <h2>

                  Priority Skills

                </h2>



                <p>

                  Skills to focus on first.

                </p>

              </div>



            </div>



            <div className="priority-skills">



              {result.priority_skills?.map(

                (skill, index) => (



                  <div

                    className="priority-item"

                    key={skill}

                  >

                    <span>

                      {index + 1}

                    </span>



                    <strong>

                      {skill}

                    </strong>

                  </div>



                )

              )}



            </div>



          </section>



          {/* ROADMAP */}

          <section className="dashboard-card">



            <div className="card-heading">



              <div>

                <h2>

                  Personalized Roadmap

                </h2>



                <p>

                  A practical learning path

                  based on your profile.

                </p>

              </div>



            </div>



            <div className="roadmap-list">



              {result.roadmap?.map(

                (week, index) => (



                  <div

                    className="roadmap-item"

                    key={index}

                  >

                    <div className="roadmap-number">

                      {index + 1}

                    </div>



                    <div>

                      <h3>

                        {week.title}

                      </h3>



                      <p>

                        {week.description}

                      </p>

                    </div>

                  </div>



                )

              )}



            </div>



          </section>



          {/* PROJECT IDEAS */}

          <section className="dashboard-card">



            <div className="card-heading">



              <div>

                <h2>

                  Recommended Projects

                </h2>



                <p>

                  Projects to strengthen

                  your portfolio.

                </p>

              </div>



            </div>



            <div className="project-grid">



              {result.project_ideas?.map(

                (project, index) => (



                  <div

                    className="project-card"

                    key={index}

                  >

                    <Lightbulb size={22} />



                    <p>

                      {project}

                    </p>

                  </div>



                )

              )}



            </div>



          </section>



          {/* INTERVIEW */}

          <section className="dashboard-card">



            <div className="card-heading">



              <div>

                <h2>

                  Interview Preparation

                </h2>



                <p>

                  Questions to practice for

                  your target role.

                </p>

              </div>



            </div>



            <div className="interview-list">



              {result.interview_questions?.map(

                (question, index) => (



                  <div

                    className="interview-item"

                    key={index}

                  >

                    <MessageSquare

                      size={18}

                    />



                    <span>

                      {question}

                    </span>

                  </div>



                )

              )}



            </div>



          </section>



        </>

      )}



      {!result && !loading && (

        <section className="placeholder-section">



          <Sparkles size={36} />



          <h2>

            Your Career Analysis

            Will Appear Here

          </h2>



          <p>

            Enter your target role and

            current skills above to begin.

          </p>



        </section>

      )}



    </div>

  );

}



export default Dashboard;