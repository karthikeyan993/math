import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import './custom.css'
import Predict from '../../components/Predict.vue'
import Recall from '../../components/Recall.vue'
import DominoChain from '../../components/DominoChain.vue'
import StaircaseSum from '../../components/StaircaseSum.vue'
import OddSquares from '../../components/OddSquares.vue'
import TrominoTiling from '../../components/TrominoTiling.vue'
import FocusTimer from '../../components/FocusTimer.vue'
import Checkpoint from '../../components/Checkpoint.vue'
import TruthTable from '../../components/TruthTable.vue'
import QuantifierGame from '../../components/QuantifierGame.vue'
import QuantifierGrid from '../../components/QuantifierGrid.vue'
import PrimeStreak from '../../components/PrimeStreak.vue'
import FactorSigns from '../../components/FactorSigns.vue'
import PartyGraph from '../../components/PartyGraph.vue'
import WasonCards from '../../components/WasonCards.vue'
import EquivalenceChecker from '../../components/EquivalenceChecker.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('Predict', Predict)
    app.component('Recall', Recall)
    app.component('DominoChain', DominoChain)
    app.component('StaircaseSum', StaircaseSum)
    app.component('OddSquares', OddSquares)
    app.component('TrominoTiling', TrominoTiling)
    app.component('FocusTimer', FocusTimer)
    app.component('Checkpoint', Checkpoint)
    app.component('TruthTable', TruthTable)
    app.component('QuantifierGame', QuantifierGame)
    app.component('QuantifierGrid', QuantifierGrid)
    app.component('PrimeStreak', PrimeStreak)
    app.component('FactorSigns', FactorSigns)
    app.component('PartyGraph', PartyGraph)
    app.component('WasonCards', WasonCards)
    app.component('EquivalenceChecker', EquivalenceChecker)
  },
} satisfies Theme
