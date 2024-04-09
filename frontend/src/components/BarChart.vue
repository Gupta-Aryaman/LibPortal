<template>
    <div class="card shadow-sm">
        <div class="card-header">
            <h4 class="card-title text-center">{{ title }}</h4>
        </div>
        <div class="card-body">
            <div class="row">
                <Bar class="m-auto" :data="barChartData" :options="barChartOptions" />
            </div>
        </div>  
        
        <!-- <pre>{{ props }}</pre> -->
    </div>
</template>

<script>
import { defineProps, toRefs, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarController, CategoryScale, LinearScale, BarElement, ArcElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarController, CategoryScale, LinearScale, BarElement, ArcElement)

export default {
    name: 'BarChart',
    components: {
        Bar
    },
    props: {
        title: {
            type: String,
            required: true
        },
        labels: {
            type: Array,
            required: true
        },
        data: {
            type: Array,
            required: true
        }
    },
    setup(props) {
        const { title, labels, data } = toRefs(props)

        const barChartData = ref({
            labels: labels.value,
            datasets: [{
                label: 'Books read per month',
                backgroundColor: ['#f87979', '#5ac18e', '#4874d9', '#f8c477', '#9f75b5'], // Different colors for each bar
                data: data.value
            }]
        })

        const barChartOptions = ref({
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    barThickness: 25 // Adjust the width of the bars
                }
            }
        })

        return { title, barChartData, barChartOptions }
    }
}
</script>

<style scoped></style>
