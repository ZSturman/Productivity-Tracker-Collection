//
//  OutputListView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/19/23.
//
import SwiftUI

struct OutputListView: View {
    @ObservedObject var vm: ActionStateViewModel
    
    var body: some View {
        Section(header: Text("Output Example")) {
            ForEach(vm.inputsArray, id: \.self) { input in
                LabeledContent {
                    Text("\(input.systemImage)")
                } label: {
                    Text(input.title)
                }
                .padding(.horizontal)
            }
            
            if vm.actionState.collectLocation {
                LabeledContent {
                    locationText(location: "Denver, CO")
                } label: {
                    Text("Location")
                }
                .padding(.horizontal)
                
                LabeledContent {
                    dateText()
                } label: {
                    Text("Date")
                }
                .padding(.horizontal)
            } else {
                LabeledContent {
                    dateText()
                } label: {
                    Text("Date")
                }
                .padding(.horizontal)
            }
            
            LabeledContent {
                timeText()
            } label: {
                Text("Time")
            }
            .padding(.horizontal)
        }
    }
    
    func dateText() -> some View {
        Text(Date(), style: .date)
            .font(.caption)
            .multilineTextAlignment(.center)
            .opacity(0.5)
    }
    
    func timeText() -> some View {
        Text(Date(), style: .time)
            .font(.caption)
            .multilineTextAlignment(.center)
            .opacity(0.5)
    }
    
    func locationText(location: String) -> some View {
        Text(location)
            .font(.caption)
            .multilineTextAlignment(.center)
            .opacity(0.5)
    }
}

struct OutputListView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationStack {
            let preview = ActionStateDataController.shared
            OutputListView(vm: .init(controller: preview))
                .environment(\.managedObjectContext, preview.viewContext)
        }
    }
}
