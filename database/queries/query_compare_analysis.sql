select count(*)
from compare_analysis ca     
where falsepositive = true 
and aantalgevonden > 0; -- 39348 vs -- 40573 

-- origineel ( filtering regelnummer verwijderd als keyword in oud en in nieuw voorkomt)
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = false; -- 8892 gevonden, en gebruik gewijzigd
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = true; -- 3126  false positive maar gewijzigd ( problematisch)
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = true
and vooraf_usage_ontbreekt = true and achteraf_nieuw_usage = false;                                  -- 3112 : gebruik verwijderd.
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = true
and not( vooraf_usage_ontbreekt = true and achteraf_nieuw_usage = false);                                  --  14 : Die anderen

select count(*) from compare_analysis ca where is_gebruik_gewijzigd = false and falsepositive = false; -- 3583 gevonden, maar niet gewijzigd. (gebruik is gelijk)
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = false and falsepositive = true; -- 37431 niet gevonden, en niet gewijzigd



-- met alternatief. ( geen filtereing regelnummer oud + regelnummer nieuw = )
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = false; -- 11998 gevonden, en gebruik gewijzigd 
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = true; -- 20  false positive maar gewijzigd Dit is problematisch
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = true and falsepositive = true
and vooraf_usage_ontbreekt = true and achteraf_nieuw_usage = false;                                  -- 12 : gebruik verwijderd.
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = false and falsepositive = false; -- 4929 gevonden, maar niet gewijzigd. (gebruik is gelijk)
select count(*) from compare_analysis ca where is_gebruik_gewijzigd = false and falsepositive = true; -- 36085 niet gevonden, en niet gewijzigd


select * from compare_analysis ca 
where is_gebruik_gewijzigd = true and falsepositive = true
-- and not( vooraf_usage_ontbreekt = true and achteraf_nieuw_usage = false)
and parse_error_vooraf = false -- 4x parse error vooraf
and parse_error_achteraf = false  -- 4x parse error achteraf
and bestandswijzing_id  not in (181379, 181382, 181386)                                -- 4x uncomment multiline comment ( bw_id 181379 (2x), 181382, 181386)
                                                                                       --  (bw_id 45183 Thread, 1814218 (2x), 181221, 181224, 188709) 
                                -- onterecht onderscheid in usage: static_usage vs instantation bw_id: 81902 81904, 81905,81906, 81907 ThreadLocalRandom
                                -- terecht onderscheid in usage: static_usage vs instantation bw_id: 269704 CompletableFuture
                                -- onterecht missen synchronized in bw_id 63517, 63518 (vanwege mulitline comment in regel? )
;