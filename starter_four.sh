mv data/four_operational.dat data/four_operational.dat_$(date +%Y_%h_%d_%H_%M)
mv data/four_contracts.dat data/four_contracts.dat_$(date +%Y_%h_%d_%H_%M)
mv data/four_cash.dat data/four_cash.dat_$(date +%Y_%h_%d_%H_%M)
mv data/four_reinoperational.dat data/four_reinoperational.dat_$(date +%Y_%h_%d_%H_%M)
mv data/four_reincontracts.dat data/four_reincontracts.dat_$(date +%Y_%h_%d_%H_%M)
mv data/four_reincash.dat data/four_reincash.dat_$(date +%Y_%h_%d_%H_%M)

for ((i=0; i<3; i++)) do
    python start.py --abce 0 --replicid $i --replicating --riskmodels 4
done
