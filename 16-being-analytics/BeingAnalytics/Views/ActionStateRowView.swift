//
//  ActionStateRowView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct ActionStateRowView: View {
    @ObservedObject var vm: ActionStateListVM
    var actionState: ActionState
    @ObservedObject var executionVM: ActionStateExecutionVM
    var dataService: DataService
    var triggerTapped: (Trigger) -> Void

    
    var triggersArray: [Trigger] {
        return Array(actionState.triggers as? Set<Trigger> ?? [])
    }


    var body: some View {
        ZStack(alignment: .leading) {
            HStack {
                ForEach(triggersArray, id: \.id) { trigger in
                    Button(action: {
                        self.triggerTapped(trigger)  // Invoke the closure
                    }, label: {
                        Image(systemName: trigger.triggerSystemImage ?? "")
                    })
                    .buttonStyle(PlainButtonStyle())
                }
                Text("\(actionState.title ?? "ActionState Item")")
                Spacer()
                Image(systemName: "chevron.right")
            }
            .swipeActions(edge: .leading) {
                ForEach(triggersArray, id: \.id) { trigger in
                    Button(action: {
                        self.triggerTapped(trigger)
                    }, label: {
                        Image(systemName: trigger.triggerSystemImage ?? "")
                    })
                }
            }
        }
    }
}
