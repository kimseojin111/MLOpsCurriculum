# Send Money 


## Parameter 
|Aa Name|Type|Description|Required|
|-------|----|-----------|--------|
|amount|int|얼만큼을 줄 것인지|-[x]|
|sender_id|int|sender 의 id|- [x]|
|receiver_id|int|receiver 의 id|- [x]| 

## Response 
|Aa Name|Type|Description|Required| 
|-------|---|------|----|
|transaction_id|int|거래를 나타내는 숫자|[x]|
|sender_id|int|sender 의 id|[x]| 
|receiver_id|int|receiver 의 id|[x]|
|amount|int|얼만큼의 돈이 오갔는지|[x]| 
|sender_money|int|거래후 sender 의 잔고|[x]|
|receiver_money|int|거래후 receiver 의 잔고|[x]|

## Error Message 
|Aa error code|message|description| 
|---|---|---|
|404|Receiver id is not found|receiver id 가 없을때|
||Sender id is not found|sender id 가 없을때|
|400|Invalid sender id|sender id 가 int 가 아닐때|
||Invalid receiver id|receiver id 가 int 가 아닐 때| 
||Invalid amount|amount 가 int 가 아닐 때| 
||sender or receiver missing|sender 나 receiver 가 없을 때|
|409|sender lack of money|sender 가 보내려는 돈이 원래 돈보다 많을 때| 