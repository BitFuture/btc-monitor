select tx_height , count(*) from tx_out group by tx_height order by create_time ;
