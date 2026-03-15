//
//  ExecutionList.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ExecutionList: View {
    @ObservedObject var viewModel: ExecutionListViewModel

    var body: some View {
        List(viewModel.executions) { execution in
            ExecutionRow(execution: execution, viewModel: ExecutionDetailViewModel(execution: execution))

        }
        .navigationBarItems(trailing: Button("Sort/Filter") {
            // Handle sort/filter logic
        })
    }
}
