//
//  SelectedTriggerListView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
// 
import SwiftUI

struct SelectedTriggerListView: View {
    @ObservedObject var vm: CreateActionStateVM
    @Binding var showAddInputSheet: Bool
    
    var body: some View {
        List {
            ForEach(vm.newActionState.triggers, id: \.id) { trigger in
                Section(header: HStack {
                    Label(trigger.title, systemImage: trigger.triggerSystemImage)
                    Spacer()
                    Button(action: {
                        vm.deleteTrigger(trigger)
                    }, label: {
                        Image(systemName: "trash.fill")
                            .foregroundColor(.gray)
                    })
                }, footer: TriggerOutputView(vm: vm, trigger: trigger)) {
                    TriggerRowView(trigger: trigger, showAddInputSheet: $showAddInputSheet, vm: vm)
                }

            }
        }
    }

}
