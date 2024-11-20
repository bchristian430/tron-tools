{
   "visible":true,
   "txID":"ecd902013a970bd798f33cc1d410d16a6899f67d04aedcb0a857378672d1115c",
   "raw_data":{
      "contract":[
         {
            "parameter":{
               "value":{
                  "amount":1568000,
                  "owner_address":"TLm2sJWHLvBWRBfmr3kssK7c6Ms5xcLar6",
                  "to_address":"TNEZ2h5PGGJcZwzLPsQHiQAGhyCJv4q17S"
               },
               "type_url":"type.googleapis.com/protocol.TransferContract"
            },
            "type":"TransferContract"
         }
      ],
      "ref_block_bytes":"ffb1",
      "ref_block_hash":"7cd20d73b1e7391c",
      "expiration":1702415178000,
      "timestamp":1702415120625
   },
   "raw_data_hex":"0a02ffb122087cd20d73b1e7391c4090b2e8fec5315a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541765beed06c3f18dc8c9160659b4c43f7804aeb46121541868877ad7c5ba98ff7b89be7a5d5612a0a7ba5f51880da5f70f1f1e4fec531",
   "signature":[
      "7e5e5473b9b0f7ac983702a037e6537e46ffbce2acd3daee17587cae96322a1f47d0776c606cdbb0fef079d0488f0fab31eb9528f380f319418a2f282b4d545e01"
   ]
}

01 02                                (Header: version, packet type)
ecd902013a970bd798f33cc1d410d16a6899f67d04aedcb0a857378672d1115c  (txID)
00 00 00 00 00 17 e6 00              (Amount)
base58-decoded owner address
base58-decoded to address
ffb1                                 (ref_block_bytes)
7cd20d73b1e7391c                     (ref_block_hash)
00 00 01 89 70 e3 6a 80              (expiration)
00 00 01 89 70 e1 25 11              (timestamp)
signature in bytes...                (signature)