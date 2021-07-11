import pandas as pd

# 2021년 7월 10일자 레포트
daily_df = pd.read_csv("data/daily_report.csv")

totals_df = (
    daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
)
totals_df = totals_df.rename(columns={"index": "condition"})

countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = (
    countries_df.groupby("Country_Region")
    .sum()
    .sort_values(by="Confirmed", ascending=False)
    .reset_index()
)

conditions = ["confirmed", "deaths", "recovered"]


def make_df(condition: str, country: str = None):
    df = pd.read_csv(f"data/time_{condition}.csv")
    if country is not None:
        df = df.loc[df["Country/Region"] == country]
    df = (
        df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"], axis=1)
        .sum()
        .reset_index(name=condition)
    )
    df = df.rename(columns={"index": "Date"})
    return df


# 국가별 레포트
def make_country_df(country: str):
    final_df = None
    for condition in conditions:
        condition_df = make_df(condition, country)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


# 세계 레포트
def make_global_df() -> pd.DataFrame:
    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df
