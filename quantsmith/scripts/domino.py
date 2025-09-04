from domino import explore, DominoSDM

dp = ...  # prepare the dataset as a Meerkat DataPanel

# split dataset
valid_dp = dp.lz[dp["split"] == "valid"]
test_dp = dp.lz[dp["split"] == "test"]

domino = DominoSDM()
domino.fit(data=valid_dp)
test_dp["slices"] = domino.transform(
    data=test_dp, embeddings="emb", targets="target", pred_probs="probs"
)
explore(data=test_dp)


from domino import DominoSlicer

domino = DominoSlicer()
domino.fit(data=valid_dp, embeddings="emb", targets="target", pred_probs="pred_probs")
dp["domino_slices"] = domino.predict(
    data=test_dp,
    embeddings="emb",
)
