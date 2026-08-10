import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="EduPro | Instructor & Course Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {background-color:#f7f8fc;}
[data-testid="stSidebar"] {background-color:#111827;}
[data-testid="stSidebar"] * {color:white !important;}
.hero {
    padding:28px 32px; border-radius:18px;
    background:linear-gradient(135deg,#172554,#312e81,#4f46e5);
    color:white; margin-bottom:22px;
}
.hero h1 {margin:0; font-size:2.2rem;}
.hero p {color:#e0e7ff;}
div[data-testid="stMetric"] {
    background:white; padding:15px; border-radius:14px;
    box-shadow:0 3px 14px rgba(0,0,0,.06);
}
.insight {
    padding:14px 16px; border-left:5px solid #4f46e5;
    background:white; border-radius:10px; margin-bottom:10px;
}
.footer {text-align:center;color:#6b7280;padding:24px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("edupro_final_data.csv")
    required = [
        "TeacherID","Expertise","YearsOfExperience","TeacherRating",
        "CourseID","CourseCategory","CourseLevel","CourseRating","TransactionID"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))

    for col in ["YearsOfExperience","TeacherRating","CourseRating","CoursePrice",
                "CourseDuration","Amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "RatingTier" not in df.columns:
        df["RatingTier"] = pd.cut(
            df["TeacherRating"],
            bins=[-np.inf,4.0,4.5,np.inf],
            labels=["Low","Mid","High"]
        )
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Put app.py and edupro_final_data.csv in the same folder.")
    st.stop()
except Exception as e:
    st.error(f"❌ Dataset error: {e}")
    st.stop()

# ---------------- Sidebar ----------------
st.sidebar.markdown("## 🎓 EduPro Analytics")
st.sidebar.caption("Instructor Performance & Course Quality Evaluation")
st.sidebar.divider()
st.sidebar.markdown("### 🔎 Filters")

expertise_options = sorted(df["Expertise"].dropna().astype(str).unique())
category_options = sorted(df["CourseCategory"].dropna().astype(str).unique())
level_options = sorted(df["CourseLevel"].dropna().astype(str).unique())

selected_expertise = st.sidebar.multiselect(
    "Instructor Expertise", expertise_options, default=expertise_options
)
selected_category = st.sidebar.multiselect(
    "Course Category", category_options, default=category_options
)
selected_level = st.sidebar.multiselect(
    "Course Level", level_options, default=level_options
)

lo = float(np.floor(df["TeacherRating"].min()*10)/10)
hi = float(np.ceil(df["TeacherRating"].max()*10)/10)

rating_range = st.sidebar.slider(
    "Teacher Rating Range",
    min_value=lo, max_value=hi, value=(lo,hi), step=0.1
)

filtered = df[
    df["Expertise"].astype(str).isin(selected_expertise)
    & df["CourseCategory"].astype(str).isin(selected_category)
    & df["CourseLevel"].astype(str).isin(selected_level)
    & df["TeacherRating"].between(rating_range[0], rating_range[1])
].copy()

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ---------------- Header ----------------
st.markdown("""
<div class="hero">
<h1>🎓 EduPro Instructor Performance Dashboard</h1>
<p>Data-driven evaluation of instructor effectiveness, course quality,
experience impact and learner engagement.</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Showing {len(filtered):,} records after applying filters.")

# ---------------- KPIs ----------------
avg_teacher = filtered["TeacherRating"].mean()
avg_course = filtered["CourseRating"].mean()
experience_corr = filtered["YearsOfExperience"].corr(filtered["TeacherRating"])
enrollments = filtered["TransactionID"].nunique()
instructors = filtered["TeacherID"].nunique()

st.subheader("📊 Executive KPIs")
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("⭐ Teacher Rating", f"{avg_teacher:.2f}/5")
c2.metric("📚 Course Rating", f"{avg_course:.2f}/5")
c3.metric("📈 Experience Impact", f"{experience_corr:.2f}" if pd.notna(experience_corr) else "N/A")
c4.metric("👥 Enrollments", f"{enrollments:,}")
c5.metric("👨‍🏫 Instructors", f"{instructors:,}")

st.divider()

tab1,tab2,tab3,tab4 = st.tabs([
    "🏆 Instructor Performance",
    "📚 Course Quality",
    "🎯 Expertise Insights",
    "💡 Findings & Recommendations"
])

# ---------------- Tab 1 ----------------
with tab1:
    st.subheader("🏆 Instructor Performance Leaderboard")

    leaderboard = (
        filtered.groupby(["TeacherID","Expertise"],as_index=False)
        .agg(
            TeacherRating=("TeacherRating","first"),
            AverageCourseRating=("CourseRating","mean"),
            Enrollments=("TransactionID","nunique"),
            Experience=("YearsOfExperience","first")
        )
        .sort_values(["TeacherRating","AverageCourseRating"],ascending=False)
    )

    leaderboard["TeacherRating"] = leaderboard["TeacherRating"].round(2)
    leaderboard["AverageCourseRating"] = leaderboard["AverageCourseRating"].round(2)

    st.dataframe(leaderboard.head(15),use_container_width=True,hide_index=True)

    left,right = st.columns(2)

    with left:
        scatter_df = filtered.drop_duplicates("TeacherID")
        fig = px.scatter(
            scatter_df,
            x="YearsOfExperience", y="TeacherRating",
            color="RatingTier", size="TeacherRating",
            hover_data=["TeacherID","Expertise"],
            title="Experience vs Teacher Rating",
            color_discrete_map={"Low":"#ef4444","Mid":"#f59e0b","High":"#22c55e"}
        )
        fig.update_layout(template="plotly_white",height=430)
        st.plotly_chart(fig,use_container_width=True)

    with right:
        tier = (
            filtered.groupby("RatingTier",observed=False)["TransactionID"]
            .nunique().reset_index(name="Enrollments")
        )
        fig = px.bar(
            tier,x="RatingTier",y="Enrollments",color="RatingTier",
            title="Enrollment Volume by Instructor Rating Tier",
            color_discrete_map={"Low":"#ef4444","Mid":"#f59e0b","High":"#22c55e"}
        )
        fig.update_layout(template="plotly_white",height=430,showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

# ---------------- Tab 2 ----------------
with tab2:
    st.subheader("📚 Course Quality Analysis")

    left,right = st.columns(2)

    with left:
        category = (
            filtered.groupby("CourseCategory",as_index=False)
            .agg(CourseRating=("CourseRating","mean"))
            .sort_values("CourseRating",ascending=False)
        )
        fig = px.bar(
            category,x="CourseRating",y="CourseCategory",
            orientation="h",text="CourseRating",
            title="Average Course Rating by Category"
        )
        fig.update_traces(texttemplate="%{text:.2f}",textposition="outside")
        fig.update_layout(template="plotly_white",height=450)
        st.plotly_chart(fig,use_container_width=True)

    with right:
        level = (
            filtered.groupby("CourseLevel",as_index=False)
            .agg(CourseRating=("CourseRating","mean"))
            .sort_values("CourseRating",ascending=False)
        )
        fig = px.bar(
            level,x="CourseLevel",y="CourseRating",
            text="CourseRating",title="Average Course Rating by Level"
        )
        fig.update_traces(texttemplate="%{text:.2f}",textposition="outside")
        fig.update_layout(template="plotly_white",height=450)
        st.plotly_chart(fig,use_container_width=True)

    heatmap = pd.pivot_table(
        filtered,values="CourseRating",
        index="CourseCategory",columns="CourseLevel",aggfunc="mean"
    )
    fig = px.imshow(
        heatmap,text_auto=".2f",aspect="auto",
        title="🔥 Course Quality Heatmap: Category × Level",
        labels={"color":"Average Rating"}
    )
    fig.update_layout(template="plotly_white",height=520)
    st.plotly_chart(fig,use_container_width=True)

# ---------------- Tab 3 ----------------
with tab3:
    st.subheader("🎯 Expertise-wise Performance")

    expertise = (
        filtered.groupby("Expertise",as_index=False)
        .agg(
            TeacherRating=("TeacherRating","mean"),
            CourseRating=("CourseRating","mean"),
            Enrollments=("TransactionID","nunique")
        )
        .sort_values("CourseRating",ascending=False)
    )
    expertise["TeacherRating"] = expertise["TeacherRating"].round(2)
    expertise["CourseRating"] = expertise["CourseRating"].round(2)
    st.dataframe(expertise,use_container_width=True,hide_index=True)

    left,right = st.columns(2)

    with left:
        fig = px.bar(
            expertise,x="CourseRating",y="Expertise",
            orientation="h",text="CourseRating",
            title="Course Quality by Expertise"
        )
        fig.update_traces(texttemplate="%{text:.2f}",textposition="outside")
        fig.update_layout(template="plotly_white",height=450)
        st.plotly_chart(fig,use_container_width=True)

    with right:
        fig = px.scatter(
            expertise,x="TeacherRating",y="CourseRating",
            size="Enrollments",hover_name="Expertise",
            title="Teacher Rating vs Course Rating by Expertise"
        )
        fig.update_layout(template="plotly_white",height=450)
        st.plotly_chart(fig,use_container_width=True)

# ---------------- Tab 4 ----------------
with tab4:
    st.subheader("💡 Data-Driven Findings")

    cat_means = filtered.groupby("CourseCategory")["CourseRating"].mean()
    exp_means = filtered.groupby("Expertise")["CourseRating"].mean()

    best_category = cat_means.idxmax()
    worst_category = cat_means.idxmin()
    best_expertise = exp_means.idxmax()

    if experience_corr > 0.2:
        exp_text = f"Experience has a positive relationship with teacher ratings (r = {experience_corr:.2f})."
    elif experience_corr < -0.2:
        exp_text = f"Experience has a negative relationship with teacher ratings (r = {experience_corr:.2f}); experience alone does not guarantee higher ratings."
    else:
        exp_text = f"Experience has a weak relationship with teacher ratings (r = {experience_corr:.2f})."

    st.markdown(
        f'<div class="insight">⭐ <b>Overall Quality:</b> '
        f'Teacher rating is <b>{avg_teacher:.2f}/5</b> and course rating is '
        f'<b>{avg_course:.2f}/5</b>.</div>',unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight">📚 <b>Best Category:</b> '
        f'<b>{best_category}</b> has the highest average course rating '
        f'({cat_means[best_category]:.2f}/5).</div>',unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight">⚠️ <b>Improvement Area:</b> '
        f'<b>{worst_category}</b> has the lowest average course rating '
        f'({cat_means[worst_category]:.2f}/5).</div>',unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight">🎯 <b>Best Expertise:</b> '
        f'<b>{best_expertise}</b> leads by average course rating.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="insight">📈 <b>Experience Insight:</b> {exp_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🚀 Recommendations")
    recs = [
        "Evaluate instructors using both teacher and course ratings.",
        "Provide targeted training to consistently lower-rated categories.",
        "Do not rely on years of experience alone when evaluating instructors.",
        "Recognize high-performing instructors and encourage knowledge sharing.",
        "Monitor rating and enrollment trends regularly to identify quality gaps."
    ]
    for i, rec in enumerate(recs,1):
        st.markdown(f"**{i}.** {rec}")

st.divider()
st.markdown(
    '<div class="footer">EduPro Instructor Performance & Course Quality Evaluation · '
    'Data Analytics Internship Project</div>',
    unsafe_allow_html=True
)
