# Lattice density bounds through dimension 48

The table covers dimensions 13–48. Gap closed is (previously established upper − our upper) / (previously established upper − named lattice lower). Displayed upper bounds are rounded upward. The lower column quotes comparison values at their source precision. [Pinned SpherePackings table](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/LATTICE_RESULTS.json) · [Exact values and proof locations](comparison.json) · [Reproduction instructions](README.md)

Dimensions **13 and 14** directly use the sharp rank-12 determinant bound from Géraud-Stewart and Naccache, including the classification and computations cited there. In dimension 13 the proved upper is **0.042023513562578**. The stronger target **0.041382759430854** still has **15 open families**, each of which can have continuous metric and gluing parameters. [Rank-12 input](https://eprint.iacr.org/2026/2825) · [Open-family list](../sections/n13/OPEN-AFTER-CONTACT-PRICES.txt)

| Dimension | Our lattice upper | Previously established upper | Named lattice lower | Gap closed | Proof |
|---:|---:|---:|---:|---:|---|
| 13 | 0.042023513562578 | 0.059905026 (all packings) | 0.029208430928108 (K₁₃) | 58.252% | [Mordell from rank 12](../sections/README.md) |
| 14 | 0.03399687961750058 | 0.034712755778 | 0.0216240960824471 | 5.469% | [Matching bound using rank 12](../sections/n14/MATCHING.md) |
| 15 | 0.02516391576531848 | 0.025511135431 | 0.0168575706567626 | 4.012% | [Certificate and census](native/minfix-lift15a-final-packing-proof.json) |
| 16 | 0.0172314323416 | 0.018655117428 | 0.0147081643974308 | 36.070% | [Published bound, external proof files](../dim16/README.md) |
| 17 | 0.01362623839310457 | 0.013832417384 | 0.0088113191823211 | 4.106% | [Certificate and census](native/minfix-oracle17a-final-packing-proof.json) |
| 18 | 0.01020980939664569 | 0.010343803448 | 0.0059283687184694 | 3.035% | [Certificate and census](native/minfix-oracle18a-final-packing-proof.json) |
| 19 | 0.00763128279574491 | 0.007808430327 | 0.0041208062797686 | 4.804% | [Certificate and census](native/nativeflag19v2-final-packing-proof.json) |
| 20 | 0.00581287464640074 | 0.005954630716 | 0.0032258614237517 | 5.195% | [Certificate and census](native/minfix-mix20a-final-packing-proof.json) |
| 21 | 0.0044091934148595 | 0.004557959175 | 0.0024658847115024 | 7.111% | [Certificate and census](native/minfix-mix21a-final-packing-proof.json) |
| 22 | 0.00333006729411059 | 0.003482932334 | 0.0021276601452758 | 11.279% | [Certificate and census](native/minfix-mix22a-final-packing-proof.json) |
| 23 | 0.00252656520190481 | 0.002608401581 | 0.001905328193426 | 11.640% | [Certificate and census](native/flag23a-final-packing-proof.json) |
| 24 | π¹²/12! | π¹²/12! | π¹²/12! (Leech) | Exact | [Exact Leech density](https://arxiv.org/abs/1603.06518) |
| 25 | 0.001286558046689577 | 0.001325232433 | 0.0006772120097731 | 5.968% | [Offline certificate](bounds-25-48.json) |
| 26 | 0.000869110293813701 | 0.000907209997 | 0.0002692200504338 | 5.972% | [Offline certificate](bounds-25-48.json) |
| 27 | 0.000580593927514536 | 0.000622938953 | 0.0001286752812026 | 8.567% | [Offline certificate](bounds-25-48.json) |
| 28 | 0.000391850205807269 | 0.000429639101 | 0.0000697587366165 | 10.500% | [Offline certificate](bounds-25-48.json) |
| 29 | 0.000271857852999427 | 0.000298025039 | 0.0000278789874568 | 9.686% | [Offline certificate](bounds-25-48.json) |
| 30 | 0.000189146062526746 | 0.000207932946 | 0.0000144286438425 | 9.709% | [Offline certificate](bounds-25-48.json) |
| 31 | 0.000135429606979112 | 0.000146087217 | 0.0000118377651859 | 7.939% | [Offline certificate](bounds-25-48.json) |
| 32 | 0.000095876900128018 | 0.000101511777 | 0.0000110407493088 | 6.228% | [Offline certificate](bounds-25-48.json) |
| 33 | 0.000073452496873459 | 0.000073827123 | 0.0000041406882896 | 0.538% | [Offline certificate](bounds-25-48.json) |
| 34 | 0.000052765505427207 | 0.000053148401 | 0.0000017669738891 | 0.745% | [Offline certificate](bounds-25-48.json) |
| 35 | 0.000037469507068664 | 0.000037664745 | 0.0000009461904151 | 0.532% | [Offline certificate](bounds-25-48.json) |
| 36 | 0.00002714588225649163623 | 0.00002727705 | 0.0000007330347783 | 0.494% | [Offline certificate](bounds-25-48.json) |
| 37 | 0.00001824556297305869842 | 0.000018268708324 | 0.0000003213562007 | 0.129% | [Offline certificate](bounds-25-48.json) |
| 38 | 0.00001234290484423536589 | 0.0000123521549304 | 0.0000002175667308912894917825935149131191 | 0.076% | [Offline certificate](bounds-25-48.json) |
| 39 | 0.0000084768372418329309 | 0.0000084799401622 | 0.0000001680281773654323233692192288852917 | 0.037% | [Offline certificate](bounds-25-48.json) |
| 40 | 0.00000597599547629544025 | 0.0000059777359372 | 0.0000001479833993134267670269835311956182 | 0.030% | [Offline certificate](bounds-25-48.json) |
| 41 | 0.00000439153950072801255 | 0.0000043927514316 | 0.000000086368303579508263682954666249428 | 0.028% | [Offline certificate](bounds-25-48.json) |
| 42 | 0.00000347235461086162196 | 0.000003473037643 | 0.000000057516899055409684372481767125146 | 0.020% | [Offline certificate](bounds-25-48.json) |
| 43 | 0.00000253598810939750405 | 0.0000025363822051 | 0.000000040157190248136217874583418475867 | 0.016% | [Offline certificate](bounds-25-48.json) |
| 44 | 0.00000176674994051655333 | 0.0000017676809433 | 0.0000000320085352655056342054972210802435 | 0.054% | [Offline certificate](bounds-25-48.json) |
| 45 | 0.00000117272262219493074 | 0.0000011728551765 | 0.0000000252315067 | 0.012% | [Offline certificate](bounds-25-48.json) |
| 46 | 0.00000077176742457565235 | 0.0000007721596228 | 0.0000000227179803 | 0.052% | [Offline certificate](bounds-25-48.json) |
| 47 | 0.00000051272563331981912 | 0.0000005130033534 | 0.0000000214660782 | 0.057% | [Offline certificate](bounds-25-48.json) |
| 48 | 0.00000034530564242393278 | 0.00000034559190288 | 0.0000000231782953 | 0.089% | [Offline certificate](bounds-25-48.json) |

The pinned lattice table starts at dimension 14. For dimension 13, the same authors give **0.059905026** for all sphere packings, which also bounds every lattice packing. The **58.252%** uses this external benchmark and the lattice lower K₁₃. This repository had already obtained a lattice-specific upper of **0.047947694667495** using its frame and glue lemmas. The periodic density of about 0.032014 uses 72 spheres per cell. [Previously established general upper](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/RESULTS.json) · [Earlier lattice certificates](../EARLIER-CERTIFICATES.md)

Dimension 24 had an exact value already, so the gap is zero. Dimension 16 carries forward the published result with its external proof dependencies. [Previously established general-packing bounds](https://github.com/alexlegeartis/SpherePackings/blob/9a9851887da20ca75825342bfb09e8ab031f4153/RESULTS.md) · [Lattice catalogue](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/density.html)
