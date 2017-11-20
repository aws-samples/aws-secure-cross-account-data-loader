select case when product_description ilike \'%milk%\' then 1 else 0 end as milk_flag
    , *
from dev.public.food_enforcement 
where left(recall_initiation_date, 4) >= 2016