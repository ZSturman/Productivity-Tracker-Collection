//
//  ListView.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ListView: View {
    @ObservedObject var sharedVM: SharedVM
    
    var body: some View {
        NavigationStack {
            List {
                ForEach(sharedVM.actionStates, id: \.id) { actionState in
                    ActionStateRowView(actionState: actionState)
                }
            }
            
        }
        .navigationTitle("ActionStates")
    }
}
