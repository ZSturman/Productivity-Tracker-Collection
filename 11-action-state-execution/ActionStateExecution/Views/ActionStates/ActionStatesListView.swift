//
//  ActionStatesListView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//

import SwiftUI

struct ActionStatesListView: View {
    @Environment(\.managedObjectContext) var managedObjectContext
    var actionStates: FetchedResults<ActionStateEntity>
    
    
    var body: some View {
            VStack {
                if actionStates.count == 0 {
                    Text("Welcome!")
                        .font(.headline)
                    Text("To get started, add a new ActionState")
                        .font(.caption)
                } else {
                    ForEach(actionStates, id: \.self) { actionState in
                        ActionStateListItemView(actionState: actionState, managedObjectContext: managedObjectContext)
                    }

                }
                
                Spacer()
            }

    }
}

