from pylections import dists

candidates = ["Parti1", "Parti2", "Parti3"]
scores = [10, 20, 9]

st = dists.FirstPastThePost(20)
st.add_score(candidates, scores)

st.calculate()