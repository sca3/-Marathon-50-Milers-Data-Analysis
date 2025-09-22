select * from Marathon.dbo.ultracleanedupdata_output

-- Number of states representated in race
select Count(Distinct State) as distinct_count from Marathon.dbo.ultracleanedupdata_output

-- Average time of Men Vs Women
select Gender, AVG(Total_minutes) as avg_time from  Marathon.dbo.ultracleanedupdata_output
group by Gender

-- Youngest and oldest race in the race
select Gender, min(Age) as youngest, max(Age) as oldest from Marathon.dbo.ultracleanedupdata_output
group by Gender

-- Average time for each age group

with age_buckets as (
select Total_Minutes,
	case when age < 30 then 'age_20-29'
		 when age < 40 then 'age_30-39'
		 when age < 50 then 'age_40-49'
		 when age < 60 then 'age_50-59'
	else 'age_60+' end as age_group
from Marathon.dbo.ultracleanedupdata_output
)

select age_group, avg(Total_Minutes) avg_race_time
from age_buckets
group by age_group


-- Top 3 Males and Females
with gender_rank as (
select rank() over (partition by Gender order by Total_Minutes asc) as gender_rank,
full_name,
gender,
total_minutes
from Marathon.dbo.ultracleanedupdata_output
)

select * from gender_rank where gender_rank <4
order by total_minutes