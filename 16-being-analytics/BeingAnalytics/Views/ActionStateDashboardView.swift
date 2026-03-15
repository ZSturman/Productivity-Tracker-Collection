//
//  ActionStateDashboardView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/15/23.
//

import SwiftUI

struct DashboardView: View {
    var actionState: ActionState
    
    // Placeholder views for visualizations
    var BarChart: some View {
        Rectangle() // Placeholder
            .fill(Color.blue)
            .frame(width: UIScreen.main.bounds.width * 0.9, height: 200)
    }

    var LineGraph: some View {
        Rectangle() // Placeholder
            .fill(Color.green)
            .frame(width: UIScreen.main.bounds.width * 0.9, height: 200)
    }

    var PieChart: some View {
        Rectangle() // Placeholder
            .fill(Color.red)
            .frame(width: UIScreen.main.bounds.width * 0.9, height: 200)
    }
    
    var body: some View {
        NavigationStack {
            VStack {
                Text("Today")
                
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 20) {
                        BarChart
                        LineGraph
                        PieChart
                    }
                    .padding()
                }
                
                // Placeholder for Map
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
                    .frame(height: 200)
                    .padding()
                
                // List of global variables
//                List {
//                    ForEach(actionState.globalvariables?.allObjects as? [GlobalVariable] ?? [], id: \.self) { variable in
//                        Text(variable.variableTitle ?? "")
//                    }
//                }
                
                Spacer()
            }
            .navigationBarTitle("Dashboard", displayMode: .inline)
        }
    }
}
