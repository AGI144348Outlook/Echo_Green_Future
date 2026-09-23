from src.echo_classroom import Classroom, blimp_item, boolq_item, zorro_pair

def test_answer_hidden_until_submission():
    row={"sentence_good":"Cats run.","sentence_bad":"Cats runs.","UID":"sva","pairID":1,"linguistics_term":"agreement"}
    room=Classroom(); item=blimp_item(row); room.enroll(item)
    public=room.administer(item.item_id)
    assert "gold" not in public and "correct" not in public
    result=room.submit(item.item_id,item.gold)
    assert result["correct"] is True
    assert room.transcript[-1]["response"] == item.gold

def test_zorro_adapter():
    item=zorro_pair("The cats runs.","The cats run.","z:1","subject_verb_agreement")
    assert item.gold in ("A","B")

def test_boolq_adapter():
    room=Classroom()
    item=boolq_item({"question":"Is water a liquid?","passage":"Water is a liquid.","answer":True},"b:1")
    room.enroll(item)
    assert room.submit("b:1","true")["correct"] is True
